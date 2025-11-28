from fastapi import APIRouter
from typing import Dict, List, Any

router = APIRouter(prefix="/components", tags=["components"])

@router.get("")
async def get_components() -> Dict[str, List[Any]]:
    """List available components"""
    return {
        "models": ["gpt-4o-mini", "gpt-4o"],
        "tools": [
            {"id": "search", "name": "Web Search", "description": "Search the web"},
            {"id": "finance", "name": "Financial Analysis", "description": "Analyze stocks"},
            {"id": "code", "name": "Code Executor", "description": "Run Python code (Secure)"}
        ],
        "memory": ["Multi-Layered Memory"],
        "safety": ["Docker Sandbox", "Guardrails"]
    }
