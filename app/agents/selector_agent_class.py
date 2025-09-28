from app.agents.base_agent import BaseAgent
from app.models.agent_context_schema import AgentContext
from app.agents.selector_agent import select_articles
import asyncio

class SelectorAgent(BaseAgent):
    """
    Agent responsible for selecting the most relevant articles from the database.
    """
    def __init__(self, name: str, max_retries: int = 2):
        super().__init__(name, max_retries)

    def execute(self, context: AgentContext, *args, **kwargs) -> bool:
        """ Agent for selecting the most relevant articles from the database.
        """
        #await asyncio.get_event_loop().run_in_executor(None, select_articles, context)
        select_articles(context)
        
        # If the number of selected articles is equal to the target articles, return True
        if len(context.article_flow.selected_articles_ids) == context.control.target_articles:
            return True
        else:
            return False
        
    def validate_input(self, context: AgentContext, *args, **kwargs) -> bool:
        """ Validate the input of the agent and return a boolean indicating if the input is valid.
        """
        
    
    