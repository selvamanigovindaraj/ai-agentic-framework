"""Multi-Agent Orchestrator using LangGraph"""
from typing import Dict, Any, List, Optional, TypedDict, Annotated
import operator
from dataclasses import dataclass
from langgraph.graph import StateGraph, END

try:
    from ..core.agent import Agent
    from ..core.state import State
except ImportError:
    pass


class AgentState(TypedDict):
    """The state of the agent workflow"""
    input: str
    output: Optional[str]
    # We can add more fields here like 'intermediate_steps', 'errors', etc.
    # Using operator.add for list fields allows appending updates
    messages: Annotated[List[Dict[str, Any]], operator.add]


from langgraph.checkpoint.memory import MemorySaver

class WorkflowGraph:
    """Orchestrator using LangGraph StateGraph"""
    
    def __init__(self):
        self.workflow = StateGraph(AgentState)
        self.entry_point = None
        self.nodes = set()
        self.checkpointer = MemorySaver()
        self.interrupt_before = []
    
    def add_node(self, node_id: str, agent: Agent, interrupt_before: bool = False) -> None:
        """Add agent node to workflow"""
        
        async def agent_node(state: AgentState) -> Dict:
            print(f"🔄 Executing node: {node_id} ({agent.name})")
            
            # Get the latest message or input as task
            task = state["input"]
            if state.get("messages"):
                last_msg = state["messages"][-1]
                if last_msg["role"] == "assistant":
                    task = f"Based on previous output: {last_msg['content'][:200]}..., continue the task."
                elif last_msg["role"] == "user":
                    task = last_msg["content"]
            
            # Execute agent
            result = await agent.execute(task=task)
            
            if result["success"]:
                return {
                    "output": result["output"],
                    "messages": [{"role": "assistant", "content": result["output"], "name": node_id}]
                }
            else:
                return {
                    "output": f"Error: {result['error']}",
                    "messages": [{"role": "system", "content": f"Error in {node_id}: {result['error']}"}]
                }

        self.workflow.add_node(node_id, agent_node)
        self.nodes.add(node_id)
        
        if interrupt_before:
            self.interrupt_before.append(node_id)
        
        # If first node, set as entry point (simple logic for now)
        if not self.entry_point:
            self.entry_point = node_id
            self.workflow.set_entry_point(node_id)
    
    def add_edge(self, from_node: str, to_node: str) -> None:
        """Add directed edge between nodes"""
        self.workflow.add_edge(from_node, to_node)
    
    def set_entry_point(self, node_id: str) -> None:
        """Explicitly set entry point"""
        self.workflow.set_entry_point(node_id)
        self.entry_point = node_id

    def add_conditional_edges(self, source: str, path: Any) -> None:
        """Add conditional edges (advanced)"""
        self.workflow.add_conditional_edges(source, path)

    async def execute(self, input_data: Dict[str, Any], thread_id: str = "1") -> Dict[str, Any]:
        """Execute workflow with persistence"""
        app = self.workflow.compile(
            checkpointer=self.checkpointer,
            interrupt_before=self.interrupt_before
        )
        
        # Initialize state
        initial_state = {
            "input": input_data.get("task", ""),
            "messages": [],
            "output": None
        }
        
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            # Run the graph
            # If resuming, we don't pass initial_state, just config and None input (or new input)
            # But for simplicity here, we always pass initial_state if starting fresh.
            # LangGraph handles state merging.
            
            final_state = await app.ainvoke(initial_state, config=config)
            return {"success": True, "output": final_state}
        except Exception as e:
            return {"success": False, "error": str(e)}


class Orchestrator:
    """Multi-agent orchestrator wrapper"""
    
    def __init__(self, workflow: WorkflowGraph):
        self.workflow = workflow
    
    async def execute(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute orchestrated workflow"""
        input_data = {"task": task, **(context or {})}
        return await self.workflow.execute(input_data)
