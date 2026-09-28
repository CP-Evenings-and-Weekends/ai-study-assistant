import os
import requests
from dotenv import load_dotenv

load_dotenv()

LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "http://localhost:11434")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

def generate_embedding(text):
    """Generate an embedding vector for a single text string."""
    response = requests.post(
        f"{LLM_API_BASE_URL}/v1/embeddings",
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": EMBEDDING_MODEL,
            "input": text,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]


def generate_embeddings_batch(texts):
    """Generate embeddings for a list of texts in a single API call."""
    if not texts:
        return []

    response = requests.post(
        f"{LLM_API_BASE_URL}/v1/embeddings",
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": EMBEDDING_MODEL,
            "input": texts,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()["data"]
    # Sort by index to maintain order
    return [item["embedding"] for item in sorted(data, key=lambda x: x["index"])]