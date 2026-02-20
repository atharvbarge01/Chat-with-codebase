# Codebase Assistant (Gemini RAG)

An advanced RAG-based system designed for navigating, explaining, and searching through large codebases with extreme token efficiency.

## Key Features

- **Dynamic Code Ingestion**: Instantly index any GitHub repository or uploaded ZIP file.
- **ScaleDown™ Compression**: A specialized syntax-aware compression engine that reduces supporting code context by **~78%**. It preserves class/function signatures and docstrings while eliding implementation details, enabling the model to "see" more of your codebase in a single query.
- **Precision Retrieval**: Uses a multi-stage pipeline involving **FAISS** vector search followed by **Cross-Encoder Re-ranking** (`ms-marco-MiniLM-L-2-v2`) for pinpoint accuracy.
- **Multilingual Support**: Powered by `tree-sitter`, supporting Python, JavaScript, Java, C++, and more.
- **Senior Architect Insights**: Configured with a system prompt that delivers deep, educational, and architectural walkthroughs of your code.

## Tech Stack

- **Core Framework**: [LlamaIndex](https://www.llamaindex.ai/)
- **LLM & Embeddings**: Google Gemini (`gemini-2.1-flash`, `text-embedding-004`)
- **Vector Database**: [FAISS](https://github.com/facebookresearch/faiss)
- **Code Parsing**: [tree-sitter](https://tree-sitter.github.io/tree-sitter/)
- **UI Framework**: [Streamlit](https://streamlit.io/)
- **Re-ranking**: Sentence-Transformers (Cross-Encoders)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/atharvbarge01/Chat-with-codebase.git
   cd Chat-with-codebase
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**:
   Create a `.env` file in the root directory and add your Google API Key:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

## 🖥 Usage

1. **Launch the application**:
   ```bash
   streamlit run app.py
   ```

2. **Index a Codebase**:
   - Use the sidebar to enter a GitHub URL or upload a ZIP.
   - Select the primary language.
   - Click **Load and Index Codebase**.

3. **Start Chatting**:
   Ask questions like:
   - "How does the authentication flow work?"
   - "Where is the database connection initialized?"
   - "Can you suggest a refactor for the ScaleDown logic?"

## ScaleDown Benchmark
The system includes a verification script to demonstrate compression efficiency:
```bash
python verify_compression.py
```
*Result: ~78.61% size reduction while preserving semantic integrity.*

## Project Structure
- `app.py`: Streamlit frontend and application orchestration.
- `chat_engine.py`: RAG pipeline, re-ranking, and ScaleDown integration.
- `compression_utils.py`: Tree-sitter logic for code extraction and summaries.
- `ingect_data.py`: Repository loading and vector store indexing.
- `requirements.txt`: Project dependencies.
