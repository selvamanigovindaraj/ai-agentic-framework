"""API Models"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AgentConfig(BaseModel):
    name: str
    instructions: str
    model: str = "gpt-4o-mini"
    tools: List[str] = []
    memory: bool = False
    safety: bool = True

class AgentCreateRequest(AgentConfig):
    pass

class AgentResponse(AgentConfig):
    id: str

class ExecuteRequest(BaseModel):
    task: str
    thread_id: Optional[str] = None

class ExecuteResponse(BaseModel):
    success: bool
    output: Any
    error: Optional[str] = None
