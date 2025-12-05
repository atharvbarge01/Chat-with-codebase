from llama_index.core import Settings, PromptTemplate
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

def setup_query_engine(index, api_key: str = None):
    """
    Sets up the query engine. Re-configures Settings to ensure the API key is active.
    """
    if index is None:
        return None

    if api_key:
        # Re-ensure settings are valid for the query phase
        Settings.llm = Gemini(model="gemini-2.5-flash", api_key=api_key)
        Settings.embed_model = GeminiEmbedding(model_name="text-embedding-004", api_key=api_key)

    # 1. Retrieval
    retriever = VectorIndexRetriever(
        index=index, 
        similarity_top_k=10, 
    )

    # 2. Re-Ranking
    reranker = SentenceTransformerRerank(
        top_n=5,
        model="cross-encoder/ms-marco-MiniLM-L-2-v2", 
    )

    template_str = (
        "You are a Senior Software Architect and Code Expert.\n"
        "Your goal is to provide comprehensive, detailed, and educational explanations.\n"
        "Analyze the provided context from the codebase deeply.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Query: {query_str}\n\n"
        "Instructions:\n"
        "1. detailed Explanation: Do NOT give short answers. Explain the 'Why' and 'How'.\n"
        "2. Architecture: If asked about the project, explain the structure, data flow, and key components.\n"
        "3. Code Walkthrough: If explaining code, break it down step-by-step.\n"
        "4. Use Formatting: Use bullet points, bold text, and code blocks to make it readable.\n"
        "Answer: "
    )
    qa_template = PromptTemplate(template_str)

    # 4. Query Engine Construction
    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        node_postprocessors=[reranker],
        text_qa_template=qa_template # Pass the custom prompt here
    )
    
    return query_engine

def get_response(query_engine, user_query):
    return query_engine.query(user_query)