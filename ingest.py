import os
import requests
from sentence_transformers import SentenceTransformer

ENDEE_URL = "http://localhost:8080"

model = SentenceTransformer("all-MiniLM-L6-v2")

DATA_FOLDER = "data"

def read_documents():
    documents = []

    for file in os.listdir(DATA_FOLDER):
        path = os.path.join(DATA_FOLDER, file)

        with open(path, "r") as f:
            text = f.read()

        documents.append({
            "id": file,
            "text": text
        })

    return documents


def generate_embedding(text):
    return model.encode(text).tolist()


def insert_into_endee(doc_id, text, vector):

    payload = {
        "id": doc_id,
        "vector": vector,
        "metadata": {
            "text": text
        }
    }

    response = requests.post(
        f"{ENDEE_URL}/vectors",
        json=payload
    )

    print("Inserted:", doc_id, response.status_code)


def main():
    docs = read_documents()

    for doc in docs:
        vector = generate_embedding(doc["text"])

        insert_into_endee(
            doc["id"],
            doc["text"],
            vector
        )
if __name__ == "__main__":
    main()
