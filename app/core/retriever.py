import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.security import get_allowed_categories
from pathlib import Path

CHROMA_DB_DIR = Path("data/processed/chroma_db")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_retriever(role: str = "admin"):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=embeddings
    )

    # Get what categories this role can see
    allowed_categories = get_allowed_categories(role)
    print(f"Role '{role}' can access: {allowed_categories}")

    # If the role has category restrictions, filter the search
    if allowed_categories and role != "admin":
        retriever = vectorstore.as_retriever(
            search_kwargs={
                "k": 4,
                "filter": {"category": {"$in": allowed_categories}}
            }
        )
    else:
        # Admin sees everything
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    print("Retriever loaded successfully.")
    return retriever