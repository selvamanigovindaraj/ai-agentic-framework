"""Vector database memory provider"""
import asyncio
from typing import Any, Dict, List
from chromadb import Client, Collection


class VectorMemory(MemoryProvider):
    """Vector database memory using ChromaDB"""
    
    def __init__(self, collection_name: str = "agent_memories", persist_dir: str = "./chroma_db"):
        self.client = Client(persist_directory=persist_dir)
        self.collection: Collection = self.client.get_or_create_collection(name=collection_name)
    
    async def store(self, memory: Dict[str, Any]) -> None:
        """Store memory as vector embedding"""
        content = memory.get("content", str(memory.get("result", "")))
        metadata = {
            "task": memory.get("task", ""),
            "timestamp": memory.get("timestamp", ""),
            "agent_id": memory.get("agent_id", "")
        }
        
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[str(hash(content))]
        )
        
        # Persist changes
        self.client.persist()
    
    async def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant memories using vector similarity"""
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        memories = []
        for i in range(len(results["documents"][0])):
            memories.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
        
        return memories
