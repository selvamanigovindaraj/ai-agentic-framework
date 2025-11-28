from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import uuid
import json
import os

# Models
from agentic_framework.server.models import AgentCreate, AgentResponse, ExecuteRequest, ExecuteResponse

# Framework Imports
from agentic_framework import Agent
from agentic_framework.llm import OpenAIClient
from agentic_framework.tools.search import SearchTool
from agentic_framework.tools.finance import FundamentalAnalysisTool
from agentic_framework.memory.multilayer import MultiLayerMemory

router = APIRouter(prefix="/agents", tags=["agents"])

# Persistence
AGENTS_DIR = "saved_agents"
os.makedirs(AGENTS_DIR, exist_ok=True)

# In-memory cache of loaded agents
loaded_agents: Dict[str, Agent] = {}
# In-memory storage for active workflows
active_workflows: Dict[str, Any] = {}

@router.get("", response_model=List[AgentResponse])
async def list_agents():
    """List saved agents"""
    agents = []
    if os.path.exists(AGENTS_DIR):
        for filename in os.listdir(AGENTS_DIR):
            if filename.endswith(".json"):
                with open(os.path.join(AGENTS_DIR, filename), "r") as f:
                    try:
                        data = json.load(f)
                        agents.append(AgentResponse(**data))
                    except json.JSONDecodeError:
                        continue
    return agents

@router.post("", response_model=AgentResponse)
async def create_agent(agent: AgentCreate):
    """Create and save an agent"""
    agent_id = f"agent_{uuid.uuid4().hex[:8]}"
    agent_data = agent.dict()
    agent_data["id"] = agent_id
    
    # Save to disk
    with open(os.path.join(AGENTS_DIR, f"{agent_id}.json"), "w") as f:
        json.dump(agent_data, f, indent=2)
        
    return AgentResponse(**agent_data)

@router.post("/{agent_id}/execute", response_model=ExecuteResponse)
async def execute_agent(agent_id: str, request: ExecuteRequest):
    """Execute an agent task"""
    # Check if this is a resume request for an existing workflow
    if agent_id in active_workflows:
        workflow_app = active_workflows[agent_id]["app"]
        current_config = active_workflows[agent_id]["config"]
        
        # Resume the workflow
        # In a real app, we would parse request.task to inject specific feedback/input
        result = await workflow_app.ainvoke(request.task, config=current_config)
        active_workflows[agent_id]["state"] = result
        
        return ExecuteResponse(
            success=True,
            output=str(result),
            cost=0.0
        )

    # Load agent config
    config_path = os.path.join(AGENTS_DIR, f"{agent_id}.json")
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="Agent not found")
        
    with open(config_path, "r") as f:
        config = json.load(f)
    
    # Check for Dynamic Workflow
    if config.get("model") == "dynamic-workflow":
        from agentic_framework.workflows.dynamic_workflow import DynamicWorkflow
        
        workflow_def = config.get("workflow", {})
        workflow = DynamicWorkflow(workflow_def)
        app = workflow.build_graph()
        
        initial_state = {
            "input": request.task, 
            "messages": [], 
            "context": {}, 
            "current_node": "start", 
            "status": "started"
        }
        thread_id = str(uuid.uuid4())
        config_run = {"configurable": {"thread_id": thread_id}}
        
        result = await app.ainvoke(initial_state, config=config_run)
        active_workflows[agent_id] = {"app": app, "config": config_run, "state": result}
        return ExecuteResponse(success=True, output=str(result), cost=0.0)

    # Default Agent Execution
    if agent_id not in loaded_agents:
        llm = OpenAIClient(model=config["model"])
        tools = []
        if "search" in config["tools"]:
            tools.append(SearchTool())
        if "finance" in config["tools"]:
            tools.append(FundamentalAnalysisTool())
            
        memory = MultiLayerMemory() if config["memory"] else None
        
        agent = Agent(
            id=agent_id,
            name=config["name"],
            instructions=config["instructions"],
            tools=tools,
            model_client=llm,
            memory=memory
        )
        loaded_agents[agent_id] = agent
    
    agent = loaded_agents[agent_id]
    
    try:
        result = await agent.execute(request.task)
        return ExecuteResponse(
            success=result["success"],
            output=result.get("output", result.get("error"))
        )
    except Exception as e:
        return ExecuteResponse(success=False, output=str(e), error=str(e))
