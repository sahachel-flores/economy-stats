# app/core/run_context.py
from app.models.agent_context_schema import AgentContext


class RunContext:
    def __init__(self, root: AgentContext):
        self.root = root          # reference to AgentContext
        self.pipeline_log = []
        self.iteration = 0
        # add per-request scratch state here
