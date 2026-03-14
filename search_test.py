from search import search_documents

query = input("Enter your question: ")

results = search_documents(query)

print("\nTop Results:\n")

for r in results:
    print("Score:", r["score"])
    print("Text:", r["metadata"]["text"])
    print("------")
