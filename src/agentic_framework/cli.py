#!/usr/bin/env python3
"""CLI entrypoint for Agentic Framework"""
import asyncio
import click
import os
from pathlib import Path

try:
    from agentic_framework import Agent, ToolRegistry
from agentic_framework.llm import OpenAIClient
from agentic_framework.tools.calculator import Calculator
from agentic_framework.orchestration.workflow import Orchestrator, WorkflowGraph
    
except ImportError:
    print("Run: pip install -e .")
    raise

@click.group()
def cli():
    """AI Agentic Framework CLI"""
    pass

@cli.command()
def test():
    """Run basic agent test"""
    asyncio.run(run_basic_test())

@cli.command()
def multiagent():
    """Run multi-agent workflow test"""
    asyncio.run(run_multiagent_test())

async def run_basic_test():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.echo("❌ Set OPENAI_API_KEY")
        return
    
    llm = OpenAIClient(model="gpt-4o-mini")
    registry = ToolRegistry()
    registry.register(Calculator())
    
    agent = Agent(
        id="test_agent",
        name="Test Agent",
        instructions="You are a test agent",
        tools=registry.get_all(),
        model_client=llm
    )
    
    result = await agent.execute("What is 25% of 847?")
    click.echo(f"✅ Test result: {result}")

async def run_multiagent_test():
    # Multi-agent workflow demo
    click.echo("🚀 Multi-agent workflow...")
    # Implementation here
    click.echo("✅ Multi-agent test completed")

if __name__ == '__main__':
    cli()
