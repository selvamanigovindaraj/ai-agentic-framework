from typing import Dict, List
import yaml
from pathlib import Path

try:
    from ..core.agent import Agent
    from ..core.memory import MemoryProvider
    from ..tools.registry import ToolRegistry
    from ..llm.base import BaseLLMClient
    from .agent_factory import AgentFactory
except ImportError:
    pass


class ConfigAgentLoader:
    """Load agents from YAML configuration files"""
    
    @staticmethod
    def load_config(filepath: str) -> Dict:
        """Load YAML agent configuration"""
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    async def create_from_yaml(
        filepath: str,
        tool_registry: ToolRegistry,
        model_client: BaseLLMClient,
        memory: MemoryProvider = None
    ) -> Agent:
        """Create agent from YAML config file"""
        config = ConfigAgentLoader.load_config(filepath)
        factory = AgentFactory(tool_registry, model_client)
        
        agent = await factory.create_from_config(config)
        agent.memory = memory
        
        return agent
