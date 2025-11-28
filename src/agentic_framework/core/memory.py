"""Memory provider interface"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class MemoryProvider(ABC):
    @abstractmethod
    async def store(self, memory: Dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        ...
