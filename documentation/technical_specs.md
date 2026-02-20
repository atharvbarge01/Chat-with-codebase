# Technical Specifications & Setup

Detailed breakdown of the project dependencies and environment configuration.

## 🛠 Tech Stack Details

| Layer | Technology | Version |
| :--- | :--- | :--- |
| **Core RAG** | LlamaIndex | Latest |
| **Embeddings** | Gemini text-embedding-004 | v1 |
| **LLM** | Gemini 1.5 Flash | v1 |
| **Vector DB** | FAISS-cpu | 1.8.0 |
| **Parsers** | Tree-Sitter | 0.21+ |
| **UI** | Streamlit | 1.30+ |

## 🔧 Environment Setup

The project requires several low-level dependencies for `tree-sitter` to function correctly.

### 1. Requirements.txt
- `llama-index-core`
- `llama-index-llms-gemini`
- `llama-index-embeddings-gemini`
- `llama-index-vector-stores-faiss`
- `tree-sitter`
- `tree-sitter-languages`
- `gitpython`
- `python-dotenv`

### 2. .env Configuration
```env
GOOGLE_API_KEY=AI... # Required for Gemini and text-embedding-004
```

## 🧠 Retrieval Pipeline configuration
In `chat_engine.py`, the following configurations govern the RAG performance:
- `similarity_top_k=10`: Initial vector search pull.
- `top_n=5`: Number of nodes after Cross-Encoder re-ranking.
- `top_n_to_keep=2`: Number of "uncompressed" nodes for the final prompt.
- `chunk_lines=40`: The granularity of the initial indexing process.
