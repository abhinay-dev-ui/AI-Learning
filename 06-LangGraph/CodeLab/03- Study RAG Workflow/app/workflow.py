"""A study RAG workflow with a retrieval subgraph and human review."""

import re

from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langgraph.errors import NodeError
from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from langgraph.types import Command, RetryPolicy, interrupt

from app.state import ResearchState, RetrievalState
from app.study_data import search_studies


# Workflow retry: weak evidence may be searched at most twice.
MAX_SEARCH_ATTEMPTS = 2

# A query without an exact study ID needs three meaningful word matches.
MIN_EVIDENCE_SCORE = 3


def with_event(state: ResearchState, event: str) -> list[str]:
    """Parent state uses replacement, so return the complete updated trace."""
    return [*state.get("trace", []), event]


def prepare(state: ResearchState) -> dict:
    """Create retrieval inputs from the user's original question."""
    # An explicit ID is reliable metadata and lets retrieval filter first.
    match = re.search(r"STUDY-\d{3}", state["question"].upper())
    return {
        "query": state["question"],
        "study_id": match.group(0) if match else "",
        "attempts": 0,
        "trace": with_event(state, "Prepared the question and optional study ID"),
    }


def retrieve(state: RetrievalState, runtime: Runtime) -> dict:
    """Invoke the search tool and convert its results back to Documents."""
    # A temporary failure is simulated only to make node retry behavior visible.
    if state["simulate_failure"]:
        raise ConnectionError("Simulated persistent search outage")
    if state["simulate_timeout"] and runtime.execution_info.node_attempt == 1:
        raise ConnectionError("Simulated temporary search outage")

    # A tool is a callable capability. This node controls when it is invoked
    # and writes the result into graph state.
    hits = search_studies.invoke(
        {"query": state["query"], "study_id": state["study_id"]}
    )
    # The tool returns serializable dictionaries. Downstream RAG nodes work
    # with LangChain Document objects, so restore that representation here.
    documents = [
        Document(
            page_content=hit["content"],
            metadata={"source": hit["source"], "study_id": hit["study_id"]},
        )
        for hit in hits
    ]
    # This is a workflow search count. It is different from node_attempt,
    # which counts infrastructure retries of this same node execution.
    attempt = state["attempts"] + 1
    return {
        "documents": documents,
        "top_score": hits[0]["score"] if hits else 0,
        "attempts": attempt,
        "trace": [f"Search {attempt} (node attempt {runtime.execution_info.node_attempt}): "
                  f"{len(documents)} hit(s), score {hits[0]['score'] if hits else 0}"],
    }


def search_error_handler(state: RetrievalState, error: NodeError) -> Command:
    """After node retries fail, record the error and leave the search subgraph."""
    return Command(
        update={
            "documents": [],
            "top_score": 0,
            "sufficient": False,
            "search_error": str(error.error),
            "attempts": state["attempts"] + 1,
            "trace": ["Search service failed after node retries"],
        },
        goto="search_failed",
    )


def search_failed(state: RetrievalState) -> dict:
    """Finish the child graph after its retry policy is exhausted."""
    return {"trace": ["Stopped retrieval after a technical failure"]}


def assess_evidence(state: RetrievalState) -> dict:
    """Decide whether the retrieved evidence is safe to send to drafting."""
    # An exact study ID is already a strong filter. A treatment-based search
    # must also meet the word-overlap threshold.
    sufficient = bool(state["documents"]) and (
        bool(state["study_id"]) or state["top_score"] >= MIN_EVIDENCE_SCORE
    )
    return {"sufficient": sufficient, "trace": [f"Evidence sufficient: {sufficient}"]}


def route_search(state: RetrievalState) -> str:
    """Choose between leaving the subgraph and rewriting the query."""
    # The attempt limit is the business termination rule for this loop.
    if state["sufficient"] or state["attempts"] >= MAX_SEARCH_ATTEMPTS:
        return "done"
    return "rewrite"


def rewrite_query(state: RetrievalState) -> dict:
    """Replace conversational terms with words used in the study files."""
    query = re.sub(r"\bhow long did\b", "duration of", state["query"], flags=re.I)
    query = re.sub(r"\blength\b", "duration", query, flags=re.I)
    query = re.sub(r"\btrial\b", "study", query, flags=re.I)
    query = re.sub(r"\blast\b", "", query, flags=re.I).strip(" ?")
    return {"query": query, "trace": [f"Rewrote query: {query}"]}


def build_retrieval_subgraph():
    """Compile the reusable retrieve → assess → optional rewrite loop."""
    builder = StateGraph(RetrievalState)

    # RetryPolicy repeats the same node after a ConnectionError. The error
    # handler supplies a controlled path after both node attempts fail.
    builder.add_node(
        "retrieve",
        retrieve,
        retry_policy=RetryPolicy(max_attempts=2, retry_on=ConnectionError),
        error_handler=search_error_handler,
    )
    builder.add_node("assess_evidence", assess_evidence)
    builder.add_node("rewrite_query", rewrite_query)
    builder.add_node("search_failed", search_failed)
    # Fixed edges always run. The conditional edge calls route_search after
    # assess_evidence and maps its label to either a node or END.
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "assess_evidence")
    builder.add_conditional_edges(
        "assess_evidence", route_search, {"rewrite": "rewrite_query", "done": END}
    )
    builder.add_edge("rewrite_query", "retrieve")
    builder.add_edge("search_failed", END)
    return builder.compile()


def route_evidence(state: ResearchState) -> str:
    """Choose drafting or a safe fallback after the child graph finishes."""
    return "draft" if state["sufficient"] else "no_evidence"


def extractive_draft(question: str, document: Document) -> str:
    """A deterministic answer so the graph works without a running LLM."""
    content = document.page_content
    if re.search(r"duration|how long|length|last", question, flags=re.I):
        match = re.search(r"duration is (\d+) months", content)
        if match:
            return f'{document.metadata["study_id"]} has a target duration of {match.group(1)} months.'
    if re.search(r"success|criterion|improvement", question, flags=re.I):
        match = re.search(r"at least (\d+) percent", content)
        if match:
            return f'The primary success criterion is at least {match.group(1)} percent improvement.'
    return "The retrieved study says: " + " ".join(content.split())


def ollama_draft(question: str, document: Document) -> str:
    """Use the same LangChain prompt → model → parser idea as the prior phase."""
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_ollama import ChatOllama

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Answer only from the supplied study text. If it does not contain the answer, say so.\nStudy text:\n{context}"),
            ("human", "{question}"),
        ]
    )
    chain = prompt | ChatOllama(model="mistral", temperature=0) | StrOutputParser()
    return chain.invoke({"context": document.page_content, "question": question})


def draft_answer(state: ResearchState) -> dict:
    """Generate one grounded draft using the selected implementation."""
    # Retrieval keeps at most one document in this learning example.
    document = state["documents"][0]
    if state["generator"] == "ollama":
        answer = ollama_draft(state["question"], document)
    else:
        answer = extractive_draft(state["question"], document)
    answer = f'{answer} [Source: {document.metadata["source"]}]'
    return {"draft": answer, "trace": with_event(state, "Drafted an answer from retrieved evidence")}


def no_evidence(state: ResearchState) -> dict:
    """Return a specific fallback for technical failure or weak evidence."""
    if state.get("search_error"):
        return {
            "draft": "The study search is unavailable right now. Please try again later.",
            "trace": with_event(state, "Used the technical-failure fallback"),
        }
    return {
        "draft": "I could not find enough evidence in the study files to answer.",
        "trace": with_event(state, "Stopped after bounded search; used a safe fallback"),
    }


def route_review(state: ResearchState) -> str:
    """Send high-impact requests to review when the caller asks for it."""
    return "review" if state["requires_review"] else "finalize"


def human_review(state: ResearchState) -> dict:
    """Pause the current thread and receive the later resume value."""
    # interrupt() persists this position through the configured checkpointer.
    # On resume, its return value is the value inside Command(resume=...).
    decision = interrupt({"question": state["question"], "draft": state["draft"]})
    return {"approved": decision == "approve", "trace": with_event(state, f"Human decision: {decision}")}


def finalize(state: ResearchState) -> dict:
    """Apply the review result and add the final AI message to state."""
    answer = state["draft"]
    if state["requires_review"] and not state.get("approved", False):
        answer = "A reviewer did not approve this answer."
    return {"answer": answer, "messages": [AIMessage(content=answer)], "trace": with_event(state, "Finalized")}


def build_workflow(checkpointer):
    """Compile the parent workflow with persistence supplied by the caller."""
    builder = StateGraph(ResearchState)

    # A compiled graph can be registered as a node. Compatible field names
    # carry data into and out of this retrieval subgraph.
    builder.add_node("prepare", prepare)
    builder.add_node("research_retrieval", build_retrieval_subgraph())
    builder.add_node("draft_answer", draft_answer)
    builder.add_node("no_evidence", no_evidence)
    builder.add_node("human_review", human_review)
    builder.add_node("finalize", finalize)

    # Parent control flow: prepare → subgraph → draft/fallback → review/finalize.
    builder.add_edge(START, "prepare")
    builder.add_edge("prepare", "research_retrieval")
    builder.add_conditional_edges(
        "research_retrieval",
        route_evidence,
        {"draft": "draft_answer", "no_evidence": "no_evidence"},
    )
    builder.add_conditional_edges(
        "draft_answer", route_review, {"review": "human_review", "finalize": "finalize"}
    )
    builder.add_edge("human_review", "finalize")
    builder.add_edge("no_evidence", "finalize")
    builder.add_edge("finalize", END)
    # The checkpointer enables thread state, interrupts, and later resume.
    return builder.compile(checkpointer=checkpointer)
