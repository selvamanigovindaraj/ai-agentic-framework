# 🤖 AI Agentic Framework

Production-ready AI Agentic Framework with composable components, dynamic agent creation, multi-agent orchestration, and enterprise features.

## 🌟 Key Features

- Composable architecture (agents, tools, memory, routing)
- Dynamic agent creation (intent-based and config-driven)
- Multi-agent orchestration (coordinator–worker, workflows)
- Multi-layer memory (semantic, episodic, procedural, short-term)
- Central tool registry with JSON-schema-based validation
- ReAct + planning-based reasoning engine
- Safety (sandbox, guardrails, cost limits) and observability (OpenTelemetry-ready)

## 🚀 Quick Start

```bash
git clone https://github.com/selvamanigovindaraj/ai-agentic-framework.git
cd ai-agentic-framework
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
cp .env.example .env
```

Fill in `.env` with your LLM and vector DB credentials, then explore `examples/` for usage.
