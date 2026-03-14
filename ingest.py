import os
import json
import requests
from sentence_transformers import SentenceTransformer

# Endee server URL
ENDEE_URL = "http://localhost:8080/api/v1"
INDEX_NAME = "documents"
METADATA_STORE = "embeddings/metadata.json"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

DATA_FOLDER = "data"


def ensure_index_exists():
    """Ensure the vector index is created in Endee."""
    print(f"Checking index '{INDEX_NAME}'...")
    payload = {
        "index_name": INDEX_NAME,
        "dim": 384,
        "space_type": "cosine",
        "M": 16,
        "ef_construction": 200
    }
    try:
        response = requests.post(f"{ENDEE_URL}/index/create", json=payload, timeout=10)
        if response.status_code == 200:
            print(f"Index '{INDEX_NAME}' created (or already exists).")
        else:
            print(f"Index status: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error ensuring index: {e}")


def read_documents():
    documents = []
    if not os.path.exists(DATA_FOLDER):
        print(f"Data folder '{DATA_FOLDER}' not found.")
        return documents

    for file in os.listdir(DATA_FOLDER):
        path = os.path.join(DATA_FOLDER, file)
        if os.path.isfile(path):
            with open(path, "r") as f:
                text = f.read()
            documents.append({"id": file, "text": text})
    return documents


def generate_embedding(text):
    return model.encode(text).tolist()


def insert_into_endee(doc_id, vector):
    """Insert a vector into Endee. Metadata stored separately in local JSON."""
    payload = {"id": doc_id, "vector": vector}
    try:
        response = requests.post(
            f"{ENDEE_URL}/index/{INDEX_NAME}/vector/insert",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to insert {doc_id}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error inserting {doc_id}: {e}")
        return False


def save_metadata(metadata_store):
    """Save document metadata to local JSON file."""
    os.makedirs(os.path.dirname(METADATA_STORE), exist_ok=True)
    with open(METADATA_STORE, "w") as f:
        json.dump(metadata_store, f, indent=2)
    print(f"Metadata saved to {METADATA_STORE}")


def main():
    ensure_index_exists()
    docs = read_documents()

    if not docs:
        print("No documents found to ingest.")
        return

    metadata_store = {}

    for doc in docs:
        print(f"Processing: {doc['id']}")
        vector = generate_embedding(doc["text"])

        if insert_into_endee(doc["id"], vector):
            # Store text in local metadata lookup
            metadata_store[doc["id"]] = {"text": doc["text"]}
            print(f"  Inserted: {doc['id']}")

    save_metadata(metadata_store)
    print(f"\nIngestion complete! {len(metadata_store)} documents indexed.")


if __name__ == "__main__":
    main()
