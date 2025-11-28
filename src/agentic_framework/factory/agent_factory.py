"""Agent Factory for dynamic creation"""
from typing import Dict, Optional
import yaml

try:
    from ..core.agent import Agent, AgentConfig
    from ..tools.registry import ToolRegistry
    from ..llm.base import BaseLLMClient
except ImportError:
    pass


class AgentFactory:
    """Factory for creating agents dynamically"""
    
    def __init__(self, tool_registry: ToolRegistry, default_model_client: BaseLLMClient):
        self.tool_registry = tool_registry
        self.default_model_client = default_model_client
        self.role_templates = self._load_role_templates()
    
    def _load_role_templates(self) -> Dict:
        """Load predefined role templates"""
        return {
            "data_analyst": {
                "instructions": "You are a data analysis expert. Analyze data and provide insights.",
                "tools": ["csv_reader", "pandas_analyzer", "chart_generator"],
                "config": {"temperature": 0.2}
            },
            "researcher": {
                "instructions": "You are a research assistant. Search and synthesize information.",
                "tools": ["web_search", "document_reader"],
                "config": {"temperature": 0.5}
            },
            "coder": {
                "instructions": "You are a coding assistant. Write and debug code.",
                "tools": ["code_executor", "file_reader", "file_writer"],
                "config": {"temperature": 0.3}
            }
        }
    
    async def create_from_config(self, config: Dict) -> Agent:
        """Create agent from configuration"""
        tools = []
        for tool_spec in config.get("tools", []):
            if isinstance(tool_spec, str):
                tool = self.tool_registry.get(tool_spec)
            elif isinstance(tool_spec, dict):
                tool = self.tool_registry.get(tool_spec["tool_id"])
            if tool:
                tools.append(tool)
        
        agent_config = AgentConfig(
            max_iterations=config.get("constraints", {}).get("max_iterations", 10),
            timeout_seconds=config.get("constraints", {}).get("timeout_seconds", 300),
            enable_sandbox=config.get("constraints", {}).get("sandbox", True),
            max_cost=config.get("constraints", {}).get("max_cost", 1.0),
            temperature=config.get("model", {}).get("temperature", 0.7)
        )
        
        return Agent(
            id=config.get("agent_id", ""),
            name=config.get("name", ""),
            instructions=config.get("instructions", ""),
            tools=tools,
            model_client=self.default_model_client,
            config=agent_config,
            metadata=config.get("metadata", {})
        )
    
    async def create_from_intent(self, user_intent: str) -> Agent:
        """Create agent from natural language intent"""
        analysis = await self._analyze_intent(user_intent)
        
        tools = self.tool_registry.discover(
            query=analysis.get("domain", ""),
            filters={"category": analysis.get("category")}
        )
        
        template_name = analysis.get("role_template", "general")
        template = self.role_templates.get(template_name, {})
        
        return Agent(
            id="",
            name=f"{template_name.title()} Agent",
            instructions=template.get("instructions", user_intent),
            tools=tools[:5],
            model_client=self.default_model_client
        )
    
    async def _analyze_intent(self, intent: str) -> Dict:
        """Analyze user intent"""
        return {
            "domain": intent,
            "category": "general",
            "role_template": "general"
        }
