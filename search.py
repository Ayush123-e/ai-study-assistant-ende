import requests
from sentence_transformers import SentenceTransformer

# Endee server
ENDEE_URL = "http://localhost:8080"

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_query(query):
    return model.encode(query).tolist()


def search_documents(query, top_k=3):

    query_vector = embed_query(query)

    payload = {
        "vector": query_vector,
        "top_k": top_k
    }

    response = requests.post(
        f"{ENDEE_URL}/query",
        json=payload
    )

    results = response.json()

    return results
