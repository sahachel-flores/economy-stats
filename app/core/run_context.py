# app/core/run_context.py
from app.agents.agent_context_class import AgentContext


class RunContext:
    def __init__(self, context: AgentContext):
        self.context = context          # reference to AgentContext
        self.pipeline_log = []
        self.iteration = 0
        # add per-request scratch state here
