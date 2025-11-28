import asyncio
import os
from agentic_framework import Agent, ToolRegistry
from agentic_framework.llm import OpenAIClient
from agentic_framework.tools.calculator import Calculator
from agentic_framework.memory.simple import SimpleMemory


print("🤖 Multi-Agent Demo")
print("="*50)

# Setup
llm_client = OpenAIClient(model="gpt-4o-mini")
registry = ToolRegistry()
registry.register(Calculator())

# Agent 1: Researcher
researcher = Agent(
    id="researcher_001",
    name="Researcher",
    instructions="You research and gather information",
    tools=registry.get_all(),
    model_client=llm_client,
    memory=SimpleMemory()
)

# Agent 2: Analyst
analyst = Agent(
    id="analyst_001",
    name="Data Analyst",
    instructions="You analyze numbers and data",
    tools=registry.get_all(),
    model_client=llm_client
)

# Simple workflow
research_result = asyncio.run(researcher.execute("Find average monthly temperature in Bangalore"))
analysis_result = asyncio.run(analyst.execute(f"Analyze: {research_result['output']}"))

print("Research:", research_result["output"][:100])
print("Analysis:", analysis_result["output"][:100])
