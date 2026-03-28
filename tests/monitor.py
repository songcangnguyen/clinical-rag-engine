import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import json
from dotenv import load_dotenv
load_dotenv()

from app.core.chain import build_chain
from app.core.security import USERS

LOG_FILE = "data/processed/usage_log.json"

def log_interaction(username, role, question, answer, latency_ms, source_count):
    """Save each interaction to a JSON log file."""
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "role": role,
        "question": question[:100],
        "answer_length": len(answer),
        "latency_ms": round(latency_ms),
        "source_count": source_count,
    }

    # Load existing log
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log = json.load(f)
    else:
        log = []

    log.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

    return entry

def run_monitored_query(username, role, question):
    """Run a question and log the performance."""
    print(f"\nUser: {username} ({role})")
    print(f"Question: {question}")

    chain, retriever = build_chain(role=role)

    # Time the response
    start = time.time()
    answer = chain.invoke(question)
    latency_ms = (time.time() - start) * 1000

    sources = retriever.invoke(question)

    entry = log_interaction(
        username=username,
        role=role,
        question=question,
        answer=answer,
        latency_ms=latency_ms,
        source_count=len(sources)
    )

    print(f"Answer: {answer[:200]}...")
    print(f"Latency: {entry['latency_ms']}ms")
    print(f"Sources used: {entry['source_count']}")
    return entry

if __name__ == "__main__":
    print("Running monitored test queries...")

    run_monitored_query(
        username="dr_smith",
        role="clinician",
        question="What clinical guidelines are mentioned in the documents?"
    )

    run_monitored_query(
        username="admin_root",
        role="admin",
        question="Summarize the key policies in the documents."
    )

    print(f"\nAll interactions logged to {LOG_FILE}")
    print("You can open this file in VSCode to review performance data.")