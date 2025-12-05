import os
import faiss
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import CodeSplitter
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

# NEW IMPORT: Manually load the parser to avoid errors
from tree_sitter_language_pack import get_parser

def create_index_from_repo(repo_path: str, code_language: str = "python", api_key: str = None):
    """
    Loads code, parses, embeds, and creates a VectorStoreIndex.
    """
    if not api_key:
        raise ValueError("API Key must be provided to create_index_from_repo")

    # Configure Settings
    Settings.llm = Gemini(model="gemini-2.5-flash", api_key=api_key)
    Settings.embed_model = GeminiEmbedding(model_name="text-embedding-004", api_key=api_key)

    print(f"--- Starting Indexing for repository: {repo_path} ---")
    
    # 1. Load Data
    documents = SimpleDirectoryReader(input_dir=repo_path, recursive=True).load_data()

    # 2. Parse Code (MANUAL FIX)
    try:
        # Explicitly get the parser for the chosen language
        parser = get_parser(code_language)
        
        code_splitter = CodeSplitter(
            language=code_language,
            chunk_lines=40,
            chunk_lines_overlap=15,
            max_chars=1500,
            parser=parser  # <--- PASS THE PARSER OBJECT DIRECTLY
        )
        nodes = code_splitter.get_nodes_from_documents(documents)
        
    except Exception as e:
        print(f"Error initializing CodeSplitter: {e}")
        # Fallback: If parsing fails, just use the documents as they are (chunking might be less perfect)
        print("Falling back to standard text splitting...")
        from llama_index.core.node_parser import TokenTextSplitter
        splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=200)
        nodes = splitter.get_nodes_from_documents(documents)

    # 3. Create Vector Store (FAISS)
    dummy_embedding = Settings.embed_model.get_text_embedding("dummy")
    d = len(dummy_embedding)
    
    faiss_index = faiss.IndexFlatL2(d)
    vector_store = FaissVectorStore(faiss_index=faiss_index)

    # 4. Create Index
    index = VectorStoreIndex(
        nodes,
        vector_store=vector_store,
    )
    
    print("--- Indexing complete. ---")
    return index