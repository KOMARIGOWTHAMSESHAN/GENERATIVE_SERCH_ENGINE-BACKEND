import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import ollama
from qdrant_client import QdrantClient

app = FastAPI(title="Generative Search Engine API")

# Enable CORS so your Next.js frontend can talk to this backend securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Qdrant Client (Using memory-mode for your 10-day local sprint setup)
try:
    qdrant_client = QdrantClient(":memory:")
    print("Qdrant initialized successfully in-memory.")
except Exception as e:
    print(f"Database connection skipped or failed: {e}")

# Define the incoming data structure using Pydantic (What the frontend must send)
class SearchRequest(BaseModel):
    query: str

def classify_intent(query: str) -> str:
    """
    NLP Gatekeeper logic: Analyzes the text to decide if the user
    wants simple 'Search' links or deep 'Research' paragraphs.
    """
    research_keywords = ["explain", "why", "how", "compare", "write", "summarize"]
    query_lower = query.lower()
    
    # Check if any research triggers match the user prompt
    if any(keyword in query_lower for keyword in research_keywords):
        return "Research"
    return "Search"

async def llama_stream_generator(prompt_text: str):
    """
    An asynchronous generator that pulls character chunks from Llama 3 
    and yields them to the network stream instantly.
    """
    try:
        # Call local Ollama chat model asynchronously
        response_stream = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt_text}],
            stream=True
        )
        
        for chunk in response_stream:
            content = chunk['message']['content']
            if content:
                yield content
                # yield a tiny sleep slice to let the event loop process other users
                await asyncio.sleep(0.01)
                
    except Exception as e:
        yield f"\n[Backend Stream Generation Error]: {str(e)}"

@app.post("/api/generative-search")
async def generative_search(request: SearchRequest):
    """
    Main Endpoint. Receives the query, classifies intent, and either
    returns data arrays (Search) or hooks up a live AI typewriter stream (Research).
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty.")
        
    intent = classify_intent(request.query)
    
    # CASE 1: Simple "Search Mode" (Google style layout data output)
    if intent == "Search":
        # Mocked DB records for your Day 4 milestone display
        mock_search_results = [
            {"title": f"Official documentation for {request.query}", "url": "https://example.com/docs", "snippet": "Found matching references inside stored collections."},
            {"title": f"Community guides on {request.query}", "url": "https://example.com/community", "snippet": "Alternative developer forum answers and syntax optimizations."}
        ]
        return {
            "intent": "Search",
            "results": mock_search_results
        }
        
    # CASE 2: "Research Mode" (ChatGPT style streaming paragraph layout)
    elif intent == "Research":
        return StreamingResponse(
            llama_stream_generator(request.query),
            media_type="text/plain"
        )

if __name__ == "__main__":
    import uvicorn
    # Launch local server on port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)