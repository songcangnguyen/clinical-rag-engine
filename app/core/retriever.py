from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path

CHROMA_DB_DIR = Path("data/processed/chroma_db")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_retriever():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=embeddings
    )
    # Return top 4 most relevant chunks for any question
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    print("Retriever loaded successfully.")
    return retriever