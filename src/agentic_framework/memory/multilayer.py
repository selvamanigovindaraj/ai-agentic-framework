from typing import List, Dict, Any
from agentic_framework.core.memory import MemoryProvider
from .semantic import SemanticMemory
from .episodic import EpisodicMemory
from .procedural import ProceduralMemory

class MultiLayerMemory(MemoryProvider):
    """
    Orchestrates multiple memory layers:
    1. Short-term (Context Buffer)
    2. Semantic (Vector DB)
    3. Episodic (Time-series DB)
    4. Procedural (Rules/Preferences)
    """
    
    def __init__(self):
        self.short_term = [] # Simple list for context
        self.semantic = SemanticMemory()
        self.episodic = EpisodicMemory()
        self.procedural = ProceduralMemory()
        
    async def store(self, memory: Dict[str, Any]) -> None:
        """Store in appropriate layers"""
        # 1. Short-term
        self.short_term.append(memory)
        if len(self.short_term) > 10:
            self.short_term.pop(0)
            
        # 2. Episodic (Log everything)
        await self.episodic.store(memory)
        
        # 3. Semantic (Only if explicitly marked or important)
        if isinstance(memory.get("content"), str):
            await self.semantic.store(memory)
            
        # 4. Procedural (Check for rule updates)
        # Simple heuristic: if memory has "type": "rule"
        if memory.get("type") == "rule":
            key = memory.get("key", "general")
            value = memory.get("content")
            self.procedural.set_preference(key, value)
            
    async def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve from Semantic memory (primary for knowledge)"""
        return await self.semantic.retrieve(query, k)
    
    def get_procedural_context(self) -> str:
        """Get procedural rules to inject into context"""
        return self.procedural.get_all_context()
    
    async def get_recent_episodes(self, k: int = 5) -> List[Dict[str, Any]]:
        """Get recent episodes"""
        return await self.episodic.retrieve("", k)
    
    async def consolidate(self):
        pass
