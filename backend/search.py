import requests

from qdrant_client import QdrantClient

def get_embedding(text):

    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text

        }
    )

    return response.json()["embedding"]

client = QdrantClient(
    host = "localhost",
    port = 6333

)

query = "how do i build APIs in python?"

query_embedding = get_embedding(query)

results = client.query_points(
    collection_name = "documents",
    query=query_embedding,
    limit = 3
)
print("\nSEARCH RESULTS\n")

for point in results.points:
    print(point.payload["text"])
