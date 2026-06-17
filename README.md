# Local Generative Search Engine Backend

An asynchronous AI-powered search engine API built with *FastAPI, **Ollama (Llama 3), and **Qdrant Vector Database*.

##  Features
- *Intent Classification:* Automatically routes simple keyword queries to traditional search layouts and complex inquiries to full AI generation.

- *Asynchronous Token Streaming:* Pipes responses token-by-token directly from local hardware using an async generator for a live typewriter UI effect.

- *Local Infrastructure:* Runs entirely on-device using Ollama—no external paid API keys required.

##  Tech Stack

- *Framework:* FastAPI (Python)
- *AI Engine:* Ollama (Llama 3 Model)
- *Database Client:* Qdrant Client

##  How to Run Locally

1. Install dependencies:
  pip install fastapi uvicorn pydantic ollama qdrant-client
      
   2. Start your local Ollama engine:

     bash
      ollama run llama3
      
   3. Launch the API server:

     bash
      python main.py
      ```
   4. Open the interactive testing panel at http://127.0.0.1:8000/docs.