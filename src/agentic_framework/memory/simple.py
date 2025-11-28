from typing import Any, Dict, List
import asyncio


class SimpleMemory(MemoryProvider):
    """Simple in-memory implementation for testing"""
    
    def __init__(self):
        self.memories: List[Dict[str, Any]] = []
    
    async def store(self, memory: Dict[str, Any]) -> None:
        self.memories.append(memory)
    
    async def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Simple keyword matching"""
        results = []
        for memory in self.memories[-100:]:  # Recent 100 memories
            if query.lower() in str(memory).lower():
                results.append(memory)
            if len(results) >= k:
                break
        return results
