"""LLM base interface."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseLLMClient(ABC):
    @abstractmethod
    async def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        """Generate a response from the LLM given chat messages."""
        raise NotImplementedError
