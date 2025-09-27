# app/agents/selector_agent.py
from app.services.logger import api_logger as logger
from app.services.openai_client import ask_openai
from app.models.agent_context_schema import AgentContext
from app.services.db_tools import get_articles_using_ids_from_db
import ast

def select_articles(candidate_articles: list[dict], context: AgentContext) -> None:
    logger.info("---------------------------------Entering select_articles function---------------------------------")
    logger.info(f"------Attempt {context.attempt}: Selecting from {len(candidate_articles)} candidates.------")
        

    
    if context.attempt == 1:
        logger.info("-------------First attempt-------------")
        instruction = f"""
        You are an expert news analyst assistant. Your task is to select the five most relevant articles for a news website 
        specializing in the U.S. economy.
        You will be given a list of objects which contains information about the news article, the structure of the object is:
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
        1. You will loop through the list of objects and analyze the content field of each article.
        2. After completing your analyzing of each article, you will select the five most relevant articles.
        3. An article can be selected only once.
        4. If one or more fields are empty, do not select the article.
        5. Return only a python list containing the ids of the five selected articles. Do not add any other text.

        Here are the list of news article:\n
        {candidate_articles}
        """

        message = {"role": "system", "content": instruction}
        

    else:
        instruction = f"""
        The editor agent has rejected the following articles with ids: {context.rejected_articles_ids}. 
        You will reselect {len(context.rejected_articles_ids)} news articles based on the feedback provided by the editor agent.
    
        Instructions:
        1. Go back to the list of candidate articles and review the content of each article. 
        2. Use the editor's feedback to reselect news articles.
        3. Do not select articles that were rejected or that were already approved. 
        4. The number of selected articles must be the same as the number of rejected articles.
        5. Return only a python list containing the ids of the selected articles. Do not add any other text.

        The ids of the approved articles are: {context.approved_articles_ids}. Make sure not to select them

        """

        logger.info(f"-------------One or more articles were rejected. Attempt {context.attempt}-------------")
        
        message = {"role": "system", "content": instruction}
        

    
    context.selector_history.append(message)

    
    # Appending selected articles to context
    result = ask_openai(context.selector_history, context)
    logger.info(f"Selector agent: The response is: {result}")
    # TODO: Create a function to convert the response to a list of ids
    result = ast.literal_eval(result)
    # Storing the ids of the selected articles by the selector agent
    context.selected_articles_ids = result
    # Calling helper function to get the content of the selected articles
    context.selected_articles_content = get_articles_using_ids_from_db(result)
    logger.info(f"The number of selected articles are: {len(context.selected_articles_ids)}\n")
 
    