# app/agents/selector_agent_class.py
from app.agents.base_agent import BaseAgent
from app.agents.agent_context_class import AgentContext
from app.services.openai_client import ask_openai
from app.services.logger import api_logger as logger
from app.services.db_tools import get_articles_using_ids_from_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.agent_exceptions import AgentExecutionError


class SelectorAgent(BaseAgent):
    """
    Agent responsible for selecting the most relevant articles from the database.
    """
    def __init__(self, name: str, max_retries: int = 2):
        super().__init__(name, max_retries)
        self.llm_client = ask_openai
        self.article_fetcher = get_articles_using_ids_from_db
        self.logger = logger

    async def execute(self, context: AgentContext, db: AsyncSession, *args, **kwargs) -> bool:
        """ 
        Agent for selecting the most relevant articles.
        """
        try:
            context.agent_states.selector.attempt = 1
            while context.agent_states.selector.attempt <= context.agent_states.selector.max_attempts:
                if not context.agent_states.selector.feedback:
                    self.logger.info(f"---------->Executing selector agent... Attempt {context.control.attempt} target articles: {context.control.target_articles}")
                    # Generating the input message
                    prompt = self.generate_input_message(context)
                    if not prompt:
                        raise AgentExecutionError("Selector agent: Error generating input message")

                    # Appending the input message to the history
                    system_message = {"role": "system", "content": prompt}
                    context.agent_states.selector.history.append(system_message)
                else:
                    # we have feedback for our agent
                    prompt = context.agent_states.selector.feedback
                    system_message = {"role": "system", "content": prompt}
                    context.agent_states.selector.history.append(system_message)
                # Asking the openai model for the response
                result = self.llm_client(context.agent_states.selector.history)
                if not result:
                    raise AgentExecutionError("Selector agent: Error ask_openai function failed to return a result")

                # Parsing the response
                parsed_result = self.parse_response(result, context)
                if not parsed_result:
                    raise AgentExecutionError("Selector agent: Error parsing the response")

                # Updating response and history to context
                context.agent_states.selector.last_response = result
                context.agent_states.selector.history.append({'role': 'assistant', 'content': result})
                context.article_flow.selected_articles_ids = parsed_result
                context.article_flow.selected_articles_content = await get_articles_using_ids_from_db(parsed_result, db)
                if not context.article_flow.selected_articles_content:
                    raise AgentExecutionError("Selector agent: Error getting the articles from the database")
                self.logger.info(f"number of needed articles: {context.control.target_articles - len(context.article_flow.approved_articles_ids)}")
                # Handling the llm response where the number of selected articles is =, <, or > than the target articles
                if len(context.article_flow.selected_articles_ids) == context.control.target_articles :
                    # Cleaning the feedback if it exists
                    if context.agent_states.selector.feedback:
                        context.agent_states.selector.feedback = None
                    return True
                elif len(context.article_flow.selected_articles_ids) < context.control.target_articles   :
                    self.logger.info(f"Selector agent: number of selected articles is less than the target articles")
                    context.agent_states.selector.feedback = "the number of selected articles is less than the target articles, read instructions again and retry again."
                    #return False
                else:
                    self.logger.info(f"Selector agent: number of selected articles is greater than the target articles")

                    context.agent_states.selector.feedback = "the number of selected articles is greater than the target articles, read instructions again and retry again."
                    #return False

                context.agent_states.selector.attempt += 1

        except Exception as e:
            self.logger.error(f"Selector agent failed to execute: {e}")
            
            return False
        return False
    
    def generate_input_message(self, context: AgentContext, feedback: str = None, *args, **kwargs) -> str:
        """ 
        Generate the input message for the selector agent.
        """
        message = ""
        if context.control.attempt == 1 and context.agent_states.selector.attempt == 1:
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
        elif context.agent_states.selector.attempt > 1 and context.agent_states.selector.feedback:
            message = f"""
            Your last response is not correct because {context.agent_states.selector.feedback}.
            """

        
        elif context.control.attempt > 1:
            message = f"""
            The editor agent has rejected {len(context.article_flow.rejected_articles_ids)} articles. 
            The following articles with ids: {context.article_flow.rejected_articles_ids} were rejected. 
            You will select {context.control.target_articles} news articles.
        
            Instructions:
            1. Revisit the list of candidate articles and review the content of each article. 
            2. Use the editor's feedback to reselect news articles.
            3. Do not select articles that were rejected or that were already approved. 
            4. The number of selected articles must be the same as the number of rejected articles.
            5. Return only a python list containing the ids of the selected articles. Do not add any other text.

            The ids of the approved articles are: {context.article_flow.approved_articles_ids}. Make sure not to select them

            """
        return message
    


        
    
    