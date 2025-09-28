# app/agents/selector_agent.py
from app.services.logger import api_logger as logger
from app.services.openai_client import ask_openai
from app.models.agent_context_schema import AgentContext
from app.services.db_tools import get_articles_using_ids_from_db
import ast

def select_articles(context: AgentContext) -> None:
    logger.info("---------------------------------Entering select_articles function---------------------------------")
    logger.info(f"------Attempt {context.control.attempt}: Selecting from {len(context.article_flow.raw_articles)} candidates.------")
        

    
    if context.control.attempt == 1:
        logger.info("-------------First attempt-------------")
        instruction = f"""
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

        message = {"role": "system", "content": instruction}
        

    else:
        instruction = f"""
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

        logger.info(f"-------------One or more articles were rejected. Attempt {context.attempt}-------------")
        
        message = {"role": "system", "content": instruction}
        

    context.agent_states.selector.history.append(message)
    # Appending system and agent messages to the history
    result = ask_openai(context.agent_states.selector.history)
    context.agent_states.selector.last_response = result
    context.agent_states.selector.history.append({'role': 'assistant', 'content': result})

    
    logger.info(f"Selector agent: The response is: {result}")

    # TODO: Verify the response is what we expect
    # TODO: Create a function to convert the response to a list of ids

    result = ast.literal_eval(result)
    # Storing the ids of the selected articles by the selector agent
    context.article_flow.selected_articles_ids = result
    # Calling helper function to get the content of the selected articles
    context.article_flow.selected_articles_content = get_articles_using_ids_from_db(result)
    logger.info(f"The number of selected articles are: {len(context.article_flow.selected_articles_ids)}\n")
 
    