import chromadb
from chromadb.utils import embedding_functions
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class SemanticMemory:
    """
    Handles semantic retrieval (vector search) for factual knowledge.
    """
    def __init__(self, collection_name: str = "agent_knowledge"):
        path = os.getenv("CHROMA_PATH", "./data/chroma_db")
        self.client = chromadb.PersistentClient(path=path)
        
        # Use default embedding function or OpenAI if key is present
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=api_key,
                model_name="text-embedding-3-small"
            )
        else:
            self.ef = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.ef
        )

    def add_fact(self, fact_id: str, content: str, metadata: Dict[str, Any] = None):
        # ChromaDB requires non-empty metadata if the argument is provided
        final_metadata = metadata or {"source": "assistant"}
        if not final_metadata:
            final_metadata = {"source": "assistant"}
            
        self.collection.add(
            documents=[content],
            metadatas=[final_metadata],
            ids=[fact_id]
        )

    def query_facts(self, query: str, n_results: int = 3) -> List[str]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []
