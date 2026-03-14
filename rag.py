from search import search_documents

def build_context(results):
    context = ""

    for r in results:
        context += r["metadata"]["text"] + "\n\n"

    return context


def generate_answer(question, context):

    answer = f"""
Question: {question}

Based on the following documents:

{context}

Answer:
The question relates to the above information. The most relevant explanation is provided using the retrieved knowledge base documents.
"""

    return answer


def rag_pipeline(question):

    # Retrieve top documents
    results = search_documents(question, top_k=3)

    # Build context
    context = build_context(results)

    # Generate answer
    answer = generate_answer(question, context)

    return answer, results
