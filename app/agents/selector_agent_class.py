# app/agents/selector_agent_class.py
from app.agents.base_agent import BaseAgent
from app.models.agent_context_schema import AgentContext
from app.agents.selector_agent import select_articles
from app.services.openai_client import ask_openai
import re
import asyncio
import ast
from app.services.logger import api_logger as logger
from app.services.db_tools import get_articles_using_ids_from_db

class SelectorAgent(BaseAgent):
    """
    Agent responsible for selecting the most relevant articles from the database.
    """
    def __init__(self, name: str, max_retries: int = 2):
        super().__init__(name, max_retries)

    def execute(self, context: AgentContext, *args, **kwargs) -> bool:
        """ 
        Agent for selecting the most relevant articles.
        """
        # Generating the input message
        instruction = self.generate_input_message(context)
        if instruction:
            message = {"role": "system", "content": instruction}
        else:
            logger.error("Error generating input message")
            return False
        # Appending the input message to the history
        context.agent_states.selector.history.append(message)
        # Asking the openai model for the response
        result = ask_openai(context.agent_states.selector.history)
        # Parsing the response
        parsed_result = self.parse_response(result, context)
        if parsed_result:
            context.agent_states.selector.last_response = result
            context.agent_states.selector.history.append({'role': 'assistant', 'content': result})
            context.article_flow.selected_articles_ids = parsed_result
            context.article_flow.selected_articles_content = get_articles_using_ids_from_db(parsed_result)
        else:
            logger.error(f"Error: parse_response() function failed to parse the response: {result}")
            return False
        
        # If the number of selected articles is equal to the target articles, return True
        # TODO: need to handle case where input number of articles is less than target articles
        if len(context.article_flow.selected_articles_ids) == context.control.target_articles:
            return True
        else:
            logger.error(f"Error the number of selected articles is not equal to the target articles: {result}")
            return False
 

    def generate_input_message(self, context: AgentContext, *args, **kwargs) -> str:
        """ 
        Generate the input message for the selector agent.
        """
        message = ""
        if context.control.attempt == 1:
            message = f"""
            You are an expert news analyst. Select the {context.control.target_articles} most relevant articles about {context.control.topic}.
            You will be given a list of objects which contains information about the news articles in the following structure:
            {{
                "id": The id of the article,
                "author": The author of the article,
                "title": The title of the article,
                "description": The description of the article,
                "url": The url of the article,
                "url_to_image": The url to the image of the article,
                "published_at": The date and time the article was published,
                "content": The content of the article.
            }}
            
            Read the following instructions carefully before selecting the articles:

            Instructions:
            1. Analyze the title and content of each article
            2. Skip articles with missing content fields.
            3. Select the {context.control.target_articles} most relevant articles.
            4. If fewer than {context.control.target_articles} qualify, select as many as possible
            5. Return ONLY a Python list of article IDs - no explanations, no other text
            6. Example output: [1, 2, 3, 4, 5]
            

            List of news articles:\n
            {context.article_flow.raw_articles}
            """
        else:
            message = f"""
            The editor agent has rejected {len(context.article_flow.rejected_articles_ids)} articles. 
            The following articles with ids: {context.article_flow.rejected_articles_ids} were rejected. 
            You will reselect {len(context.article_flow.rejected_articles_ids)} news articles.
        
            Instructions:
            1. Revisit the list of candidate articles and review the content of each article. 
            2. Use the editor's feedback to reselect news articles.
            3. Do not select articles that were rejected or that were already approved. 
            4. The number of selected articles must be the same as the number of rejected articles.
            5. Return only a python list containing the ids of the selected articles. Do not add any other text.

            The ids of the approved articles are: {context.approved_articles_ids}. Make sure not to select them

            """
        return message
        

        
    
    