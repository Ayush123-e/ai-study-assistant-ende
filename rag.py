from search import search_documents


def build_context(results):
    texts = []

    for r in results:
        text = r.get("metadata", {}).get("text", "")
        if text:
            texts.append(text)

    return texts


def extract_relevant_sentences(question, documents):

    question_words = set(question.lower().split())

    relevant = []

    for doc in documents:
        sentences = doc.split(".")
        for s in sentences:
            words = set(s.lower().split())

            if len(question_words.intersection(words)) > 0:
                relevant.append(s.strip())

    return relevant


def generate_answer(question, documents):

    if not documents:
        return f"No relevant information found for: {question}"

    sentences = extract_relevant_sentences(question, documents)

    if not sentences:
        sentences = documents

    summary = ". ".join(sentences[:3])

    answer = f"""
Question: {question}

Answer:
{summary}
"""

    return answer


def rag_pipeline(question):

    results = search_documents(question, top_k=3)

    documents = build_context(results)

    answer = generate_answer(question, documents)

    return answer, results