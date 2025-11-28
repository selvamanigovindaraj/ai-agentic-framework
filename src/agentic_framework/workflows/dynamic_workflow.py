from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from agentic_framework.llm.openai_client import OpenAIClient
# Assuming we have a way to load tools, for now we'll mock or import specific ones
# from agentic_framework.tools import TOOL_REGISTRY 

class WorkflowState(TypedDict):
    input: str
    messages: List[Dict[str, str]]
    context: Dict[str, Any]
    current_node: str
    status: str

class DynamicWorkflow:
    def __init__(self, workflow_def: Dict[str, Any]):
        self.nodes_def = workflow_def.get("nodes", [])
        self.edges_def = workflow_def.get("edges", [])
        self.llm = OpenAIClient()
        self.tools = {} # In real app, load from registry

    def _get_node_by_id(self, node_id: str) -> Optional[Dict]:
        for node in self.nodes_def:
            if node["id"] == node_id:
                return node
        return None

    async def execute_llm_node(self, state: WorkflowState, config: Dict) -> Dict:
        print(f"--- Executing LLM Node: {config.get('label', 'Unnamed')} ---")
        prompt_template = config.get("prompt", "")
        # Simple variable substitution from context
        # e.g. "Analyze {ticker}" -> "Analyze AAPL"
        # This is a basic implementation
        prompt = prompt_template
        for key, value in state.get("context", {}).items():
            prompt = prompt.replace(f"{{{key}}}", str(value))
            
        # Also append input if it's the first node
        if not state["messages"]:
             prompt += f"\nInput: {state['input']}"

        response = await self.llm.generate([{"role": "user", "content": prompt}])
        
        new_messages = state["messages"] + [{"role": "assistant", "content": response["content"]}]
        # Update context with result for future nodes to use? 
        # For now, just store in messages.
        return {"messages": new_messages, "current_node": config["id"]}

    async def execute_tool_node(self, state: WorkflowState, config: Dict) -> Dict:
        print(f"--- Executing Tool Node: {config.get('tool', 'Unknown')} ---")
        # Mock implementation for now
        tool_name = config.get("tool")
        result = f"Mock result for {tool_name} with input {state['input']}"
        
        new_messages = state["messages"] + [{"role": "system", "content": f"Tool Output: {result}"}]
        return {"messages": new_messages, "current_node": config["id"]}

    async def execute_hitl_node(self, state: WorkflowState, config: Dict) -> Dict:
        print(f"--- HITL Node: {config.get('message', 'Approval Required')} ---")
        # This node doesn't do much, it just serves as a pause point.
        # The graph will be compiled to interrupt after this node.
        return {"status": "waiting_for_approval", "current_node": config["id"]}

    def build_graph(self):
        workflow = StateGraph(WorkflowState)
        
        hitl_nodes = []

        # Add Nodes
        for node in self.nodes_def:
            node_id = node["id"]
            node_type = node["type"]
            node_config = node.get("data", {}) # React Flow puts config in 'data'
            # Also support direct config for backend-only testing
            if not node_config: 
                node_config = node.get("config", {})
            
        # Helper factory to bind config correctly
        def create_wrapper(func, node_cfg):
            async def wrapper(state, config=None):
                # config is LangChain's RunConfig (unused here but required by signature)
                return await func(state, node_cfg)
            return wrapper

        # Add Nodes
        for node in self.nodes_def:
            node_id = node["id"]
            node_type = node["type"]
            node_config = node.get("data", {}) 
            if not node_config: 
                node_config = node.get("config", {})
            
            # Inject ID into config for reference
            node_config["id"] = node_id

            if node_type == "llm":
                workflow.add_node(node_id, create_wrapper(self.execute_llm_node, node_config))
                
            elif node_type == "tool":
                workflow.add_node(node_id, create_wrapper(self.execute_tool_node, node_config))
                
            elif node_type == "hitl":
                workflow.add_node(node_id, create_wrapper(self.execute_hitl_node, node_config))
                hitl_nodes.append(node_id)

        # Add Edges
        for edge in self.edges_def:
            source = edge["source"]
            target = edge["target"]
            workflow.add_edge(source, target)
            
        # Determine Entry Point (Node with no incoming edges)
        # For simplicity, assume the first node in the list or explicit start
        if self.nodes_def:
            workflow.set_entry_point(self.nodes_def[0]["id"])
            
        # Add END edges for leaf nodes
        # LangGraph might handle this, but explicit is better
        # Find nodes that are targets but not sources?
        # Actually, LangGraph requires explicit END edge or it stops if no edge?
        # Let's assume the last node connects to END if no other edge.
        
        # Compile
        # We interrupt AFTER HITL nodes so the user can review the state AT that node
        app = workflow.compile(
            interrupt_after=hitl_nodes
        )
        return app
