from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import requests

client = QdrantClient(
    host="localhost",
    port=6333
)

def get_embedding(text):

    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    return response.json()["embedding"]


text = """
FastAPI is a modern Python framework.

It supports routing.

It supports dependency injection.

It supports authentication.

It is widely used for APIs.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(text)

points = []

for i, chunk in enumerate(chunks):

    embedding = get_embedding(chunk)

    points.append(
        PointStruct(
            id=100 + i,
            vector=embedding,
            payload={
                "text": chunk
            }
        )
    )

client.upsert(
    collection_name="documents",
    points=points
)

print("Chunks stored successfully")
