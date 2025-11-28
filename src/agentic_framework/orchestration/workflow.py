"""Multi-Agent Orchestrator"""
from typing import Dict, Any, List, Optional
import asyncio
from dataclasses import dataclass

try:
    from ..core.agent import Agent
    from ..core.state import State
    from ..tools.registry import ToolRegistry
except ImportError:
    pass


@dataclass
class Node:
    """Workflow node (agent or function)"""
    id: str
    agent: Agent
    inputs: List[str] = None
    outputs: List[str] = None


class WorkflowGraph:
    """Directed acyclic graph for multi-agent workflows"""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, List[str]] = {}
    
    def add_node(self, node_id: str, agent: Agent) -> None:
        """Add agent node to workflow"""
        self.nodes[node_id] = Node(id=node_id, agent=agent)
        self.edges[node_id] = []
    
    def add_edge(self, from_node: str, to_node: str) -> None:
        """Add directed edge between nodes"""
        if from_node in self.nodes and to_node in self.nodes:
            self.edges[from_node].append(to_node)
    
    async def execute(self, input_data: Dict[str, Any], start_node: str = None) -> Dict[str, Any]:
        """Execute workflow from start node"""
        state = State({"input": input_data})
        
        # Find start node (no incoming edges)
        if not start_node:
            start_node = next(iter(self.nodes))
        
        current_nodes = [start_node]
        visited = set()
        
        while current_nodes:
            next_nodes = []
            
            for node_id in current_nodes:
                if node_id in visited:
                    continue
                
                visited.add(node_id)
                node = self.nodes[node_id]
                
                print(f"🔄 Executing node: {node_id} ({node.agent.name})")
                
                # Execute agent
                result = await node.agent.execute(
                    task=state.data.get("current_task", "Process input"),
                    context=state.data
                )
                
                if result["success"]:
                    state.update({node_id: result["output"]})
                    
                    # Add next nodes
                    for next_node in self.edges[node_id]:
                        next_nodes.append(next_node)
                        state.data["current_task"] = f"Use {node_id} output: {result['output'][:100]}..."
                else:
                    print(f"❌ Node {node_id} failed: {result['error']}")
                    return {"success": False, "error": result["error"]}
            
            current_nodes = next_nodes
        
        return {"success": True, "output": state.data}


class Orchestrator:
    """Multi-agent orchestrator with workflow support"""
    
    def __init__(self, workflow: WorkflowGraph):
        self.workflow = workflow
    
    async def execute(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute orchestrated workflow"""
        input_data = {"task": task, **(context or {})}
        return await self.workflow.execute(input_data)
