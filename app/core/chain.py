import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.retriever import load_retriever
from app.core.security import redact_pii

load_dotenv()

PROMPT_TEMPLATE = """
You are a clinical documentation assistant for a healthcare organization.
Use ONLY the context below to answer the question.
If the answer is not in the context, say "I could not find this in the provided documents."
Always cite which part of the document your answer came from.
Never reveal any personal patient information.

Context:
{context}

Question:
{question}

Answer:
"""

def format_docs(docs):
    # Redact PII from every chunk before sending to the LLM
    return "\n\n".join(redact_pii(doc.page_content) for doc in docs)

def build_chain(role: str = "admin"):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
    )

    # Load retriever filtered by role
    retriever = load_retriever(role=role)

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    print(f"RAG chain built for role: {role}")
    return chain, retriever