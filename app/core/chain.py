import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.retriever import load_retriever

load_dotenv()

PROMPT_TEMPLATE = """
You are a clinical documentation assistant for a healthcare organization.
Use ONLY the context below to answer the question.
If the answer is not in the context, say "I could not find this in the provided documents."
Always cite which part of the document your answer came from.

Context:
{context}

Question:
{question}

Answer:
"""

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_chain():
    # Load the LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
    )

    # Load the retriever
    retriever = load_retriever()

    # Build the prompt
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    # Modern LangChain chain using LCEL (pipe syntax)
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    print("RAG chain built successfully.")
    return chain