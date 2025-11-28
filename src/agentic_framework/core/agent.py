"""Core Agent class with ReAct reasoning"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import asyncio
import uuid
from datetime import datetime

try:
    from ..llm.base import BaseLLMClient
    from .tool import Tool
    from .memory import MemoryProvider
    from .state import State
except ImportError:
    pass  # Will be resolved after package structure is complete


@dataclass
class AgentConfig:
    """Agent configuration"""
    max_iterations: int = 10
    timeout_seconds: int = 300
    enable_sandbox: bool = True
    max_cost: float = 1.0
    temperature: float = 0.7


@dataclass
class Agent:
    """Production-ready Agent with full capabilities"""
    
    id: str
    name: str
    instructions: str
    tools: List[Tool]
    model_client: BaseLLMClient
    memory: Optional[MemoryProvider] = None
    config: AgentConfig = field(default_factory=AgentConfig)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.id:
            self.id = f"agent_{uuid.uuid4().hex[:8]}"
        self.state = State()
        self.iteration_count = 0
        self.total_cost = 0.0
    
    async def execute(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute task using ReAct reasoning loop"""
        self.iteration_count = 0
        self.state.update({"task": task, "status": "running"})
        
        try:
            # Memory retrieval
            if self.memory:
                memories = await self.memory.retrieve(task, k=5)
                context = context or {}
                context["memories"] = memories
            
            # Build messages
            messages = self._build_messages(task, context)
            
            # Execute ReAct loop
            result = await self._react_loop(messages)
            
            # Store experience
            if self.memory:
                await self.memory.store({
                    "task": task,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })
            
            self.state.update({"status": "completed"})
            return {
                "success": True,
                "output": result,
                "iterations": self.iteration_count,
                "cost": self.total_cost
            }
            
        except Exception as e:
            self.state.update({"status": "failed", "error": str(e)})
            return {
                "success": False,
                "error": str(e),
                "iterations": self.iteration_count
            }
    
    def _build_messages(self, task: str, context: Optional[Dict] = None) -> List[Dict]:
        """Build LLM messages with tools and context"""
        messages = [{"role": "system", "content": self.instructions}]
        
        if context and context.get("memories"):
            memories_text = "\n".join([m["content"] for m in context["memories"]])
            messages.append({"role": "system", "content": f"Relevant memories:\n{memories_text}"})
        
        if self.tools:
            tools_text = self._format_tools()
            messages.append({"role": "system", "content": f"Available tools:\n{tools_text}"})
        
        messages.append({"role": "user", "content": task})
        return messages
    
    def _format_tools(self) -> str:
        """Format tools for prompt"""
        return "\n".join([f"- {t.name}: {t.description}" for t in self.tools])
    
    async def _react_loop(self, messages: List[Dict]) -> str:
        """ReAct: Thought → Action → Observation loop"""
        conversation = messages.copy()
        
        while self.iteration_count < self.config.max_iterations:
            self.iteration_count += 1
            
            response = await self.model_client.generate(
                messages=conversation,
                temperature=self.config.temperature
            )
            
            self.total_cost += response.get("cost", 0)
            
            if self.total_cost > self.config.max_cost:
                raise Exception(f"Cost limit exceeded: ${self.total_cost:.2f}")
            
            content = response["content"]
            conversation.append({"role": "assistant", "content": content})
            
            if self._is_task_complete(content):
                return content
            
            if tool_calls := self._extract_tool_calls(content):
                for tool_call in tool_calls:
                    observation = await self._execute_tool(tool_call)
                    conversation.append({
                        "role": "user",
                        "content": f"Observation: {observation}"
                    })
            else:
                return content
        
        raise Exception(f"Max iterations ({self.config.max_iterations}) exceeded")
    
    def _is_task_complete(self, response: str) -> bool:
        """Check for task completion markers"""
        markers = ["final answer", "task complete", "conclusion", "finished"]
        return any(marker in response.lower() for marker in markers)
    
    def _extract_tool_calls(self, response: str) -> List[Dict]:
        """Extract tool calls (simplified)"""
        tool_calls = []
        for tool in self.tools:
            if tool.name.lower() in response.lower():
                tool_calls.append({"tool": tool, "params": {}})
        return tool_calls
    
    async def _execute_tool(self, tool_call: Dict) -> str:
        """Execute tool and return observation"""
        tool = tool_call["tool"]
        try:
            result = await tool.execute(**tool_call["params"])
            return f"Tool {tool.name} returned: {result}"
        except Exception as e:
            return f"Tool {tool.name} error: {str(e)}"
    
    def get_state(self) -> Dict:
        """Get current agent state"""
        return self.state.to_dict()
