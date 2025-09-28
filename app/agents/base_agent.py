from abc import ABC, abstractmethod
from app.models.agent_context_schema import AgentContext


class BaseAgent(ABC):
    def __init__(self, name: str, max_retries: int = 2):
        self.name = name
        self.max_retries = max_retries

    @abstractmethod
    def execute(self, context: AgentContext, *args, **kwargs) -> bool:
        """
        Execure the agent's logic and return a boolean indicating if the execution was successful.
        """
        pass
    
    # @abstractmethod
    # def validate_input(self, context: AgentContext, *args, **kwargs) -> bool:
    #     """
    #     Validate the input of the agent and return a boolean indicating if the input is valid.
    #     """
    #     pass
    
    # @abstractmethod
    # def validate_output(self, context: AgentContext) -> bool:
    #     """
    #     Validate the output of the agent and return a boolean indicating if the output is valid.
    #     """

    #     pass

    # @abstractmethod
    # def run_with_retry(self, context: AgentContext, *args, **kwargs) -> bool:
    #     """
    #     Run the agent with retry logic.
    #     """
    #     pass
    
    # @abstractmethod
    # def get_agent_stats(self, context: AgentContext) -> dict:
    #     """
    #     Get the stats of the agent.
    #     """
    #     pass
    
    # @abstractmethod
    # def get_agent_history(self, context: AgentContext) -> list[dict]:
    #     """
    #     Get the history of the agent.
    #     """