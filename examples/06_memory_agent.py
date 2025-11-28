import asyncio
import os
from dotenv import load_dotenv
from agentic_framework import Agent, ToolRegistry
from agentic_framework.llm import OpenAIClient
from agentic_framework.memory.multilayer import MultiLayerMemory

load_dotenv()

print("🧠 Multi-Layered Memory Agent System")
print("="*50)

# Setup
llm_client = OpenAIClient(model="gpt-4o-mini")
memory = MultiLayerMemory()

# Create Agent with Memory
agent = Agent(
    id="learner_01",
    name="Learner",
    instructions="You are a learning agent. Remember facts and use them.",
    tools=[],
    model_client=llm_client,
    memory=memory
)

async def main():
    # 1. Teach the agent a fact (Semantic Memory)
    print("\n📚 Teaching agent...")
    fact = "The capital of Mars in 2050 is Elon City."
    await memory.store({
        "content": fact,
        "metadata": {"source": "user", "topic": "mars"},
        "type": "fact"
    })
    print(f"Stored fact: {fact}")
    
    # 2. Perform a task (Episodic Memory)
    print("\n🎬 Performing task...")
    task = "What is the capital of Mars?"
    result = await agent.execute(task)
    if result["success"]:
        print(f"Agent Answer: {result['output']}")
    else:
        print(f"Agent Execution Failed: {result['error']}")
    
    # 3. Verify Episodic Log
    print("\n📜 Checking Episodic Memory (Recent Events)...")
    episodes = await memory.get_recent_episodes(k=2)
    for ep in episodes:
        print(f"- [{ep['timestamp']}] {ep['type']}: {str(ep['content'])[:50]}...")

    # 4. Verify Semantic Retrieval
    print("\n🔍 Checking Semantic Retrieval...")
    knowledge = await memory.retrieve("Mars capital")
    for k in knowledge:
        print(f"- Found: {k['content']} (Metadata: {k['metadata']})")

if __name__ == "__main__":
    asyncio.run(main())
