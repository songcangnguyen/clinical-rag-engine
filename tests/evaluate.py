import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from app.core.chain import build_chain
from tests.golden_dataset import GOLDEN_DATASET

print("Building RAG chain...")
chain, retriever = build_chain(role="admin")

print("Running questions through the chain...")
results = []
for item in GOLDEN_DATASET:
    question = item["question"]
    reference = item["reference_answer"]

    # Get the answer from your RAG chain
    answer = chain.invoke(question)

    # Get the source chunks that were used
    source_docs = retriever.invoke(question)
    contexts = [doc.page_content for doc in source_docs]

    results.append({
        "user_input": question,
        "response": answer,
        "retrieved_contexts": contexts,
        "reference": reference
    })
    print(f"Answered: {question[:60]}...")

print("\nRunning Ragas evaluation...")

# Wrap models for Ragas
llm = LangchainLLMWrapper(ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
))
embeddings = LangchainEmbeddingsWrapper(
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
)

# Build the dataset
dataset = Dataset.from_list(results)

# Run evaluation
scores = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy],
    llm=llm,
    embeddings=embeddings
)

print("\n=============================")
print("   EVALUATION RESULTS")
print("=============================")
faithfulness_score = scores['faithfulness']
relevancy_score = scores['answer_relevancy']

if isinstance(faithfulness_score, list):
    faithfulness_score = sum(faithfulness_score) / len(faithfulness_score)
if isinstance(relevancy_score, list):
    relevancy_score = sum(relevancy_score) / len(relevancy_score)

print(f"Faithfulness:      {faithfulness_score:.2f}  (higher = less hallucination)")
print(f"Answer Relevancy:  {relevancy_score:.2f}  (higher = more on-topic)")
print("=============================")

# CI/CD gate — fail if scores drop below threshold
FAITHFULNESS_THRESHOLD = 0.7
RELEVANCY_THRESHOLD = 0.7

# NEW - replace with these
if faithfulness_score < FAITHFULNESS_THRESHOLD:
    print(f"\nFAIL: Faithfulness {faithfulness_score:.2f} is below {FAITHFULNESS_THRESHOLD}")
    sys.exit(1)

if relevancy_score < RELEVANCY_THRESHOLD:
    print(f"\nFAIL: Answer relevancy {relevancy_score:.2f} is below {RELEVANCY_THRESHOLD}")
    sys.exit(1)

print("\nPASS: All scores are above thresholds. Safe to deploy!")