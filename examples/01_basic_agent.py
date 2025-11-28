"""Basic working example of the agent framework"""
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Add to path for development
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from agentic_framework import Agent, ToolRegistry
    from agentic_framework.llm import OpenAIClient
    from agentic_framework.tools.calculator import Calculator
except ImportError as e:
    print(f"Import error: {e}")
    print("Run: pip install -e .")
    exit(1)


async def main():
    """Basic agent example"""
    print("🤖 AI Agentic Framework - Basic Example")
    print("="*80)

    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Please set OPENAI_API_KEY in .env")
        print("cp .env.example .env")
        return

    # Initialize LLM
    print("🔌 Initializing OpenAI client...")
    llm_client = OpenAIClient(model="gpt-4o-mini")

    # Create tool registry
    print("🛠️  Creating tool registry...")
    registry = ToolRegistry()
    calculator = Calculator()
    registry.register(calculator)

    print(f"✅ Registered {len(registry.get_all())} tools")

    # Create agent
    print("🤖 Creating Math Assistant agent...")
    agent = Agent(
        id="math_assistant_001",
        name="Math Assistant",
        instructions="""
You are a helpful math assistant. 

Use the calculator tool for:
- Basic operations (+, -, *, /)
- Square root (sqrt)

Always show your work and explain the steps.
Provide the final answer clearly.
        """.strip(),
        tools=registry.get_all(),
        model_client=llm_client
    )

    # Test tasks
    tasks = [
        "What is 15% of 2847?",
        "Calculate compound interest for $10,000 at 5% annual rate for 3 years",
        "What's the square root of 144?",
        "If I have 250 apples and eat 3 per day, how many days until I run out?"
    ]

    print("\n🚀 Running tasks...")
    for i, task in enumerate(tasks, 1):
        print(f"\n--- Task {i}: {task} ---")
        
        result = await agent.execute(task)
        
        if result["success"]:
            print(f"✅ SUCCESS (Iterations: {result['iterations']}, Cost: ${result['cost']:.4f})")
            print(f"📝 Output: {result['output'][:200]}...")
        else:
            print(f"❌ FAILED: {result['error']}")

    print("\n🎉 Example completed!")


if __name__ == "__main__":
    asyncio.run(main())
