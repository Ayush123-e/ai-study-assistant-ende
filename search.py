import json
import requests
import msgpack
from sentence_transformers import SentenceTransformer

# Endee server
ENDEE_URL = "http://localhost:8080/api/v1"
INDEX_NAME = "documents"
METADATA_STORE = "embeddings/metadata.json"

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_metadata():
    """Load local metadata store."""
    try:
        with open(METADATA_STORE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Metadata store not found at {METADATA_STORE}. Run ingest.py first.")
        return {}
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return {}


def embed_query(query):
    return model.encode(query).tolist()


def search_documents(query, top_k=3):
    metadata = load_metadata()
    query_vector = embed_query(query)

    payload = {"vector": query_vector, "k": top_k}

    try:
        response = requests.post(
            f"{ENDEE_URL}/index/{INDEX_NAME}/search",
            json=payload,
            timeout=10
        )

        if response.status_code != 200:
            print(f"Search failed: {response.status_code} - {response.text}")
            return []

        # Server returns MsgPack encoded: [[score, id, meta_bin, meta_str, ...], ...]
        raw_results = msgpack.unpackb(response.content)

        results = []
        for item in raw_results:
            score = item[0]
            doc_id = item[1]

            # Look up the actual text from our local metadata store
            doc_meta = metadata.get(doc_id, {})
            text = doc_meta.get("text", f"[No text found for {doc_id}]")

            results.append({
                "score": score,
                "id": doc_id,
                "metadata": {"text": text}
            })

        return results

    except Exception as e:
        print(f"Search failed: {e}")
        return []
