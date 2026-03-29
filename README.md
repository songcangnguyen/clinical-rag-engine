# 🏥 Secure Clinical RAG Engine

> Enterprise-grade document intelligence for healthcare — built with Python, LangChain, and Llama 3.3.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![LangChain](https://img.shields.io/badge/LangChain-latest-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3-green)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

---

## 📌 Overview

Clinical teams waste countless hours searching through unstructured medical documents — policies, guidelines, and payer contracts. This application solves that problem with a secure, AI-powered "Ask My Docs" interface that retrieves precise answers with verifiable citations.

Unlike a standard chatbot, this system is built with real enterprise constraints:

- 🔐 **Role-Based Access Control (RBAC)** — doctors, analysts, HR and admins each see only the documents they are authorized to access
- 🛡️ **Automatic PII Redaction** — SSNs, phone numbers, emails and medical record numbers are scrubbed before any data reaches the LLM
- 📎 **Citation Enforcement** — every answer includes the exact source chunks it was drawn from
- 🧪 **Automated Evaluation Pipeline** — Ragas scores every answer for faithfulness and relevancy, blocking deployment if quality drops
- 📊 **Full Observability** — LangSmith traces every query with latency, token usage and cost

---

## 🖥️ Screenshots

### Login screen
<img width="905" height="594" alt="image" src="https://github.com/user-attachments/assets/4fa6cab1-fc06-4762-ad80-25082a2c1d44" />

### Chat interface with citations
<img width="1800" height="852" alt="image" src="https://github.com/user-attachments/assets/7cd778fa-c160-47cd-8e86-ca5b4c7fa94c" />


### LangSmith monitoring dashboard
<img width="1674" height="780" alt="image" src="https://github.com/user-attachments/assets/2a1966f2-df34-4aac-8e55-4396e4ffa988" />


---

## 🏗️ Architecture
```
User question
     │
     ▼
RBAC layer (filter by role)
     │
     ▼
Hybrid retriever (ChromaDB vector search)
     │
     ▼
PII redaction
     │
     ▼
Llama 3.3 via Groq (answer generation)
     │
     ▼
Answer + citations returned to user
     │
     ▼
LangSmith (trace logged) + Ragas (quality scored)
```

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Framework | LangChain | Connects all pipeline components |
| LLM | Llama 3.3 70B via Groq | Ultra-low latency inference |
| Vector DB | ChromaDB | Semantic document search |
| Embeddings | HuggingFace all-MiniLM-L6-v2 | Text to vector conversion |
| PDF Parsing | Docling + PyPDF | Clinical PDF ingestion |
| Frontend | Streamlit | Web UI with simulated RBAC login |
| Evaluation | Ragas | Faithfulness and relevancy scoring |
| Monitoring | LangSmith | Query tracing and cost analysis |
| Language | Python 3.11+ | Core application language |

---

## 📁 Project Structure
```
clinical-rag-engine/
├── app/
│   ├── core/
│   │   ├── ingest.py        # PDF loading, chunking, embedding
│   │   ├── retriever.py     # ChromaDB search with role filtering
│   │   ├── chain.py         # RAG pipeline (retriever + LLM)
│   │   └── security.py      # RBAC, authentication, PII redaction
│   └── ui/
│       └── interface.py     # Streamlit web application
├── data/
│   ├── raw/                 # Source PDF documents
│   └── processed/           # ChromaDB vector store + usage logs
├── tests/
│   ├── golden_dataset.py    # Reference Q&A pairs for evaluation
│   ├── evaluate.py          # Ragas evaluation pipeline
│   └── monitor.py           # Performance monitoring script
├── .env                     # API keys (never committed to Git)
└── README.md
```

---

## ⚡ Project

### Prerequisites
- Python 3.11+
- Git
- A free [Groq API key](https://console.groq.com)
- A free [LangSmith API key](https://smith.langchain.com)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/clinical-rag-engine.git
cd clinical-rag-engine
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install langchain langchain-community langchain-groq langchain-core
pip install langchain-text-splitters langchain-huggingface
pip install chromadb sentence-transformers pypdf docling
pip install streamlit python-dotenv rank_bm25
pip install ragas datasets
```

### 4. Set up environment variables
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_key_here
LANGSMITH_API_KEY=your_langsmith_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=clinical-rag-engine
```

### 5. Add your documents
Drop any clinical PDF files into the `data/raw/` folder.

### 6. Ingest your documents
```bash
python -m app.core.ingest
```

### 7. Launch the app
```bash
streamlit run app/ui/interface.py
```

Open your browser to `http://localhost:8501`

---

## 👥 Demo Accounts

| Username | Password | Role | Document Access |
|---|---|---|---|
| dr_smith | clinic123 | Clinician | Clinical docs, guidelines, pharmacy |
| analyst_jane | data456 | Informatics | Data dictionaries, clinical, guidelines |
| hr_bob | hr789 | HR | Payroll, HR policy |
| admin_root | admin000 | Admin | All documents |

---

## 🧪 Running Evaluations
```bash
# Run Ragas quality evaluation
python tests\evaluate.py

# Run performance monitoring
python tests\monitor.py
```

Expected output:
```
=============================
   EVALUATION RESULTS
=============================
Faithfulness:      0.91  (higher = less hallucination)
Answer Relevancy:  0.87  (higher = more on-topic)
=============================
PASS: All scores are above thresholds. Safe to deploy!
```

---

## 🔐 Security Features

**Role-Based Access Control** — document retrieval is filtered at the database query level, meaning unauthorized users cannot access restricted chunks even through prompt injection attempts.

**PII Redaction** — the following patterns are automatically detected and redacted before any text reaches the LLM:
- Social Security Numbers
- Phone numbers
- Email addresses
- Dates of birth
- Medical Record Numbers (MRN)

**No hallucination policy** — the system prompt instructs the LLM to respond with "I could not find this in the provided documents" rather than generating an answer not grounded in the source material.

---

## 📈 Monitoring

Every query is automatically traced in LangSmith with:
- Full input and output
- Retrieval latency
- Token usage and estimated cost
- Source documents used

Local performance logs are saved to `data/processed/usage_log.json`.

---

## 🚀 Future Improvements

- [ ] Deploy to Azure Container Apps
- [ ] Add BM25 hybrid search alongside vector search
- [ ] Connect to a real authentication provider (Auth0, Azure AD)
- [ ] Add a Power BI dashboard for executive reporting
- [ ] Support DOCX and HTML document formats
