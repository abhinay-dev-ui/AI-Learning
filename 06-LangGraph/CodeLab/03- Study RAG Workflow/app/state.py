"""The data that passes between graph nodes."""

import operator
from typing import Annotated, NotRequired, TypedDict

from langchain_core.documents import Document
from langgraph.graph import MessagesState


class ResearchState(MessagesState):
    """State shared by the parent graph from invocation to final answer."""

    # Values supplied when the application invokes the graph.
    question: str
    requires_review: bool
    generator: str
    simulate_timeout: bool
    simulate_failure: bool

    # Values added as nodes execute. NotRequired means callers do not need to
    # provide them in the initial input.
    query: NotRequired[str]
    study_id: NotRequired[str]
    attempts: NotRequired[int]
    documents: NotRequired[list[Document]]
    top_score: NotRequired[int]
    sufficient: NotRequired[bool]
    search_error: NotRequired[str]
    draft: NotRequired[str]
    answer: NotRequired[str]
    approved: NotRequired[bool]

    # The parent graph replaces this list with the extended list returned by
    # with_event(). MessagesState separately supplies the messages field and
    # its message-aware reducer.
    trace: list[str]


class RetrievalState(TypedDict):
    """The child graph accumulates events before returning one result to its parent."""

    # Inputs copied from the parent graph.
    question: str
    query: str
    study_id: str
    attempts: int
    simulate_timeout: bool
    simulate_failure: bool

    # operator.add is the reducer: each child node can return one new event,
    # and LangGraph appends it to the existing list.
    trace: Annotated[list[str], operator.add]

    # Outputs produced while the retrieval subgraph runs.
    documents: NotRequired[list[Document]]
    top_score: NotRequired[int]
    sufficient: NotRequired[bool]
    search_error: NotRequired[str]
