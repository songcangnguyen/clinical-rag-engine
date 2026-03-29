import os 
from pathlib import Path 
from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings

# --- Configuration ---
RAW_DATA_DIR = Path("data/raw")
CHROMA_DB_DIR = Path("data/processed/chroma_db")

# --- Step 1: Load PDFs ---
def load_documents():
    docs = []
    pdf_files = list(RAW_DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDFs found in data/raw/ folder!")
        return []

    for pdf_path in pdf_files:
        print(f"Loading: {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()

        for page in pages:
            page.metadata["category"] = "clinical"

        docs.extend(pages)

    print(f"Loaded {len(docs)} pages total.")
    return docs

# --- Step 2: Split into chunks ---
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,       # each chunk = ~500 characters
        chunk_overlap=50,     # chunks overlap by 50 chars so context isn't lost
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")
    return chunks

# --- Step 3: Store in vector database ---
def store_in_chroma(chunks):
    print("Loading embedding model (this may take a minute first time)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Storing chunks in ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_DIR)
    )
    print(f"Done! Stored in {CHROMA_DB_DIR}")
    return vectorstore

# --- Run everything ---
if __name__ == "__main__":
    docs = load_documents()
    if docs:
        chunks = split_documents(docs)
        store_in_chroma(chunks)
        print("\nIngestion complete! Your documents are searchable.")