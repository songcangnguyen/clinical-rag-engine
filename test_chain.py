from app.core.chain import build_chain
from app.core.retriever import load_retriever

chain = build_chain()
retriever = load_retriever()

question = "What is your current database layout?"

print(f"\nQuestion: {question}")
print("\nThinking...\n")

# Get the answer
answer = chain.invoke(question)
print("Answer:")
print(answer)

# Show sources separately
print("\nSources used:")
docs = retriever.invoke(question)
for i, doc in enumerate(docs):
    print(f"\n--- Source {i+1} ---")
    print(doc.page_content[:300])