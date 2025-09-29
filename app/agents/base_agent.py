from abc import ABC, abstractmethod
from app.models.agent_context_schema import AgentContext
from app.services.logger import agent_logger as logger
import re
import ast

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

    def parse_response(self, response: str, context: AgentContext, *args, **kwargs) -> list[int]:
        """ 
        Parse the response from the selector agent and return a boolean indicating if the response is valid.
        """

        try:
            # method1 parse the response as a list
            list_pattern = r'\[[\d,\s]*\]'
            match = re.search(list_pattern, response)
            if match:
                try:
                    parsed = ast.literal_eval(match.group())
                    if isinstance(parsed, list) and all(isinstance(item, int) for item in parsed):
                        logger.info(f"Parsed list: {parsed} successfully")
                        context.article_flow.selected_articles_ids = parsed
                        return parsed
                except Exception as e:
                    logger.error(f"Error parsing response with method1: {e}")
                    
            # method2 parse the response as a list of numbers
            numbers = re.findall(r'\d+', response)
            if numbers:
                result = [int(x) for x in numbers]
                logger.info(f"Parsed list: {result} successfully")
                context.article_flow.selected_articles_ids = result
                return result
            else:
                logger.error("Error parsing response with method2")
            
            # method3 Look for comma-separated numbers
            comma_pattern = r'(\d+(?:\s*,\s*\d+)*)'
            comma_matches = re.findall(comma_pattern, response)
            for match in comma_matches:
                try:
                    numbers = [int(x.strip()) for x in match.split(',')]
                    if len(numbers) > 0:
                        logger.info(f"Parsed list: {numbers} successfully")
                        context.article_flow.selected_articles_ids = numbers
                        return numbers
                except Exception as e:
                    logger.error(f"Error parsing response with method3: {e}")
                    continue

            logger.error("Error parsing response with all methods")
            return []
    
        except Exception as e:
            logger.error(f"Unexpected Error occured while parsing response: {e}")
            return []
    
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