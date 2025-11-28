import pytest
import os
from dotenv import load_dotenv
from agentic_framework import Agent, ToolRegistry
from agentic_framework.llm import OpenAIClient
from agentic_framework.tools.calculator import Calculator
from agentic_framework.memory.simple import SimpleMemory
from agentic_framework.core.tool import Tool
from agentic_framework.observability.telemetry import instrument_agent

load_dotenv()

# --- Tool Testing ---
class MockTool(Tool):
    def __init__(self):
        super().__init__(name="mock_tool", description="A mock tool", category="test")
    
    async def execute(self, param: str = "") -> str:
        if param == "error":
            raise ValueError("Mock error")
        return f"Processed: {param}"

@pytest.mark.asyncio
async def test_tool_execution_e2e():
    """Test tool execution and error handling"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")

    llm = OpenAIClient(model="gpt-4o-mini")
    registry = ToolRegistry()
    registry.register(MockTool())

    agent = Agent(
        id="tool_agent",
        name="Tool Agent",
        instructions="Use the mock_tool. If asked to error, pass 'error'. IMPORTANT: After getting the tool result, you MUST output the result and stop.",
        tools=registry.get_all(),
        model_client=llm
    )

    # Success case
    result = await agent.execute("Use mock_tool with input 'hello'")
    if result["success"]:
        assert "Processed: hello" in result["output"] or "Processed: hello" in str(result)
    else:
        pytest.fail(f"Agent execution failed: {result.get('error')}")

    # Error case
    result_error = await agent.execute("Use mock_tool with input 'error'")
    # The agent should report the error in its thought process or final answer
    if result_error["success"]:
        assert "Mock error" in result_error["output"] or "error" in result_error["output"].lower()
    else:
        assert "Mock error" in result_error.get("error", "") or "error" in result_error.get("error", "").lower()

# --- Memory Testing ---
@pytest.mark.asyncio
async def test_agent_memory_e2e():
    """Test agent memory persistence within session"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")

    llm = OpenAIClient(model="gpt-4o-mini")
    agent = Agent(
        id="memory_agent",
        name="Memory Agent",
        instructions="You remember things. Use the provided memories to answer questions.",
        tools=[],
        model_client=llm,
        memory=SimpleMemory()
    )

    # First interaction
    await agent.execute("My name is Alice.")
    
    # Second interaction
    result = await agent.execute("What is my name?")
    assert "Alice" in result["output"]

# --- Orchestration Testing ---
@pytest.mark.asyncio
async def test_orchestration_e2e():
    """Test simple multi-agent handoff (simulated)"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")

    llm = OpenAIClient(model="gpt-4o-mini")
    
    # Agent 1: Planner
    planner = Agent(
        id="planner",
        name="Planner",
        instructions="Plan a task. Output 'Plan: <plan>'",
        tools=[],
        model_client=llm
    )
    
    # Agent 2: Executor
    executor = Agent(
        id="executor",
        name="Executor",
        instructions="Execute the plan. Output 'Executed: <plan>'",
        tools=[],
        model_client=llm
    )
    
    # Workflow
    plan_result = await planner.execute("Plan to buy groceries")
    plan = plan_result["output"]
    
    exec_result = await executor.execute(f"Execute this plan: {plan}")
    assert "Executed" in exec_result["output"]

# --- Safety Testing ---
@pytest.mark.asyncio
async def test_safety_cost_limit_e2e():
    """Test cost limits"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")

    llm = OpenAIClient(model="gpt-4o-mini")
    
    # Create agent with very low cost limit
    agent = Agent(
        id="safety_agent",
        name="Safety Agent",
        instructions="Generate a very long story.",
        tools=[],
        model_client=llm
    )
    agent.config.max_cost = 0.0000001 # Extremely low limit
    
    result = await agent.execute("Write a long story about a dragon.")
    
    # Should fail or return error about cost
    assert result["success"] is False
    assert "Cost limit exceeded" in result["error"]

# --- Observability Testing ---
@pytest.mark.asyncio
async def test_observability_e2e():
    """Test telemetry instrumentation"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")

    # Enable telemetry for this test
    os.environ["ENABLE_TELEMETRY"] = "true"
    
    llm = OpenAIClient(model="gpt-4o-mini")
    agent = Agent(
        id="obs_agent",
        name="Observability Agent",
        instructions="Say hello.",
        tools=[],
        model_client=llm
    )
    
    # Instrument agent
    agent = instrument_agent(agent)
    
    # Execute
    result = await agent.execute("Hello")
    assert result["success"] is True
    
    # Verify telemetry object is attached (mock verification since we can't easily check OTLP export in unit test)
    assert hasattr(agent, "telemetry")
    assert agent.telemetry is not None
