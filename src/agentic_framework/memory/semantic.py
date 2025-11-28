"""Semantic Memory using ChromaDB"""
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from agentic_framework.core.memory import MemoryProvider

class SemanticMemory(MemoryProvider):
    """Semantic memory using Vector DB (ChromaDB)"""
    
    def __init__(self, collection_name: str = "agent_knowledge", persist_dir: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
    async def store(self, memory: Dict[str, Any]) -> None:
        """Store text with metadata"""
        content = memory.get("content", "")
        metadata = memory.get("metadata", {})
        # Ensure ID
        mem_id = memory.get("id", str(hash(content)))
        
        # Ensure metadata is not empty (ChromaDB requirement in some versions)
        if not metadata:
            metadata = {"type": "memory"}
            
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[mem_id]
        )
        
    async def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve semantically similar memories"""
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        memories = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                memories.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "id": results["ids"][0][i]
                })
        return memories
