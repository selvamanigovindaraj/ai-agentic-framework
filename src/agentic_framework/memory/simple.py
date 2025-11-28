from typing import Any, Dict, List
import asyncio


from agentic_framework.core.memory import MemoryProvider
class SimpleMemory(MemoryProvider):
    """Simple in-memory implementation for testing"""
    
    def __init__(self):
        self.memories: List[Dict[str, Any]] = []
    
    async def store(self, memory: Dict[str, Any]) -> None:
        self.memories.append(memory)
    
    async def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Simple keyword matching"""
        results = []
        # Strip punctuation and split
        import string
        query_clean = query.translate(str.maketrans('', '', string.punctuation))
        query_terms = query_clean.lower().split()
        
        for memory in self.memories[-100:]:  # Recent 100 memories
            memory_str = str(memory).lower()
            # Match if query is in memory OR any query term is in memory (excluding common stop words)
            if query.lower() in memory_str or any(term in memory_str for term in query_terms if len(term) > 3):
                results.append(memory)
            if len(results) >= k:
                break
        print(f"DEBUG: Found {len(results)} memories")
        return results
