from app.agents.base_agent import BaseAgent
from app.models.agent_context_schema import AgentContext
from app.services.openai_client import ask_openai
from app.services.logger import agent_logger as logger
from app.services.db_tools import get_articles_using_ids_from_db
from app.db.session import SessionLocal
from app.exceptions.agent_exceptions import AgentExecutionError

class EditorAgent(BaseAgent):
    """
    Agent responsible for editing the articles.
    """
    def __init__(self, name: str, max_retries: int = 2):
        super().__init__(name, max_retries)
        self.llm_client = ask_openai
        self.article_fetcher = get_articles_using_ids_from_db
        self.logger = logger
    
    def execute(self, context: AgentContext, db: SessionLocal, *args, **kwargs) -> bool:
        """
        Agent for editing the articles.
        """
        try:
            context.agent_states.editor.attempt = 1
            while context.agent_states.editor.attempt <= context.agent_states.editor.max_attempts:
                self.logger.info(f"---------------->Executing editor agent... Attempt {context.agent_states.editor.attempt}")
                # Generate input message
                instruction = self.generate_input_message(context)
                if not instruction:
                    raise AgentExecutionError("Editor agent: Error generating input message")
                message = {"role": "system", "content": instruction}
                # appending messages to the editor history
                context.agent_states.editor.history.append(message)

                # LLM client call  
                result = self.llm_client(context.agent_states.editor.history)
                if not result:
                    raise AgentExecutionError("Editor agent: Error ask_openai function failed to return a result")
                
                # Parsing the response
                parsed_result = self.parse_response(result, context)
                if not parsed_result:
                    raise AgentExecutionError("Editor agent: Error parsing the response")

                # adding appove articles and history
                context.article_flow.approved_articles_ids.extend(parsed_result)
                context.agent_states.editor.history.append({'role': 'assistant', 'content': result})

                # Handling the llm response where the number of approved articles is =, <, or > than the target articles
                if len(context.article_flow.approved_articles_ids) == context.control.target_articles:
                    
                    context.agent_states.editor.last_response = result
                    context.agent_states.editor.history.append({'role': 'assistant', 'content': result})
                    context.article_flow.approved_articles_content.append(get_articles_using_ids_from_db(context.article_flow.approved_articles_ids, db))
                    return True
                elif len(context.article_flow.approved_articles_ids) > context.control.target_articles:
                    logger.info(f"The selector agent aproved {len(context.article_flow.approved_articles_ids)}...... removing some ids")
                    context.article_flow.approved_articles_ids = context.article_flow.approved_articles_content[:context.control.target_articles]
                    return True
                else:
                    self.logger.info(f"Editor agent - parsed result: {parsed_result}")
                    self.logger.info(f"Editor agent - selected articles ids: {context.article_flow.selected_articles_ids}")
                    for a in context.article_flow.selected_articles_ids:
                        if a not in parsed_result:
                            context.article_flow.rejected_articles_ids.append(a)
                    self.logger.info(f"Editor agent - rejected articles ids: {context.article_flow.rejected_articles_ids}")
                    return False
                context.agent_states.editor.attempt += 1

        except Exception as e:
            logger.error(f"Fatal error occured with Editor agent: {e}")
            return False
        
        return True
    
    def generate_input_message(self, context: AgentContext, *args, **kwargs) -> str:
        """
        Generate the input message for the editor agent.
        """
        if context.control.attempt == 1:
            instruction = f""" You are an experienced news editor. Your task is to review a list of objects which contains information about the 
            news articles related to the topic: {context.control.topic}.
            The structure of the objects is as follows:

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

            Instructions:
            1. Analyze the title and content of each article
            2. After completing your analysis, determine if the articles are relevant to the main topic.
            3. Return ONLY a Python list of article IDs - no explanations, no other text
            4. Example output: [1, 2, 3, 4, 5]

            List of selected news articles by the selector agent:\n
            {context.article_flow.selected_articles_content}

            """
        else:
            instruction = f""" 
            You approved the articles with id: {context.article_flow.approved_articles_ids}.
            The selector agent selected the articles with ids: {context.article_flow.selected_articles_ids}.
            Using the previous instructions, review the list of articles and select the id of {context.control.target_articles - len(context.article_flow.approved_articles_ids)} article(s).
            from selected news articles.

            Remember that the target number of selected articles' id is {context.control.target_articles}.
            Do not approver more articles than this value.

            List news articles:\n
            {context.article_flow.selected_articles_content}
            """
        
        return instruction