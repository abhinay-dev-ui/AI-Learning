from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama


# ---------------------------------------------------------
# Step 1: Prompt Template
# ---------------------------------------------------------

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question clearly and briefly.

    Question:
    {question}
    """
)


# ---------------------------------------------------------
# Step 2: Model
# ---------------------------------------------------------

model = ChatOllama(
    model="mistral",
)


# ---------------------------------------------------------
# Step 3: Output Parser
# ---------------------------------------------------------
#
# Chat models normally return an AIMessage object.
#
# StrOutputParser converts that into a plain string.
# ---------------------------------------------------------

parser = StrOutputParser()


# ---------------------------------------------------------
# Step 4: LCEL Chain
# ---------------------------------------------------------

chain = (
    prompt
    | model
    | parser
)


# ---------------------------------------------------------
# Step 5: Invoke
# ---------------------------------------------------------

result = chain.invoke(
    {
        "question": "What is Retrieval Augmented Generation?"
    }
)


print("\nResult:")
print(result)