"""OpenTelemetry integration"""
import os
from opentelemetry import trace

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

try:
    from ..core.agent import Agent
except ImportError:
    pass


class Telemetry:
    """OpenTelemetry integration for agent observability"""
    
    def __init__(self, service_name: str = "agentic-framework"):
        self.service_name = service_name
        self.tracer = None
        self._init_tracer()
    
    def _init_tracer(self):
        """Initialize OpenTelemetry tracer"""
        if os.getenv("ENABLE_TELEMETRY", "false").lower() == "true":
            provider = TracerProvider()
            provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
            trace.set_tracer_provider(provider)
            self.tracer = trace.get_tracer(self.service_name)
    
    def start_agent_span(self, agent: Agent, task: str):
        """Start span for agent execution"""
        if not self.tracer:
            return None
        
        span = self.tracer.start_span(f"agent.execute", attributes={
            "agent.id": agent.id,
            "agent.name": agent.name,
            "task": task[:100]
        })
        return span


def instrument_agent(agent: Agent) -> Agent:
    """Add telemetry to existing agent"""
    telemetry = Telemetry()
    agent.telemetry = telemetry
    return agent
