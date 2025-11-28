"""OpenAI LLM Client Implementation"""
from typing import Any, Dict, List
import os
from openai import AsyncOpenAI

from .base import BaseLLMClient


class OpenAIClient(BaseLLMClient):
    """OpenAI LLM client with cost tracking"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4", base_url: str = None):
        self.client = AsyncOpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url
        )
        self.model = model
    
    async def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        """Generate response from OpenAI"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2000),
            stream=False
        )
        
        content = response.choices[0].message.content
        
        # Approximate cost calculation
        if content:
            tokens = len(content.split()) * 1.3  # Rough estimate
        else:
            tokens = 0
            
        cost = tokens * 0.00001  # Approximate $0.01 per 1000 tokens
        
        return {
            "content": content or "",  # Ensure content is at least empty string
            "tokens": tokens,
            "cost": cost
        }
