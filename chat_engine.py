from llama_index.core import Settings, PromptTemplate
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore, QueryBundle
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from typing import List, Optional
from compression_utils import extract_code_summary

class ScaleDownPostprocessor(BaseNodePostprocessor):
    """
    Compresses non-top-ranked nodes to preserve context while saving tokens.
    """
    top_n_to_keep: int = 1

    def _postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle] = None
    ) -> List[NodeWithScore]:
        # Always keep the top N nodes fully intact
        for i, node_with_score in enumerate(nodes):
            if i < self.top_n_to_keep:
                continue
            
            # Compress the rest
            original_text = node_with_score.node.get_content()
            language = node_with_score.node.metadata.get("language", "python")
            
            compressed_text = extract_code_summary(original_text, language)
            
            # Update node content with a header indicating it was compressed
            node_with_score.node.set_content(
                f"--- [CONTEXT COMPRESSED] ---\n{compressed_text}\n---"
            )
            
        return nodes

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

    # 3. ScaleDown Compression
    compressor = ScaleDownPostprocessor(top_n_to_keep=2)

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
        node_postprocessors=[reranker, compressor],
        text_qa_template=qa_template # Pass the custom prompt here
    )
    
    return query_engine

def get_response(query_engine, user_query):
    return query_engine.query(user_query)