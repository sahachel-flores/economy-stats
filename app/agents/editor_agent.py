# app/agents/selector_agent.py
from app.services.logger import api_logger as logger
from app.services.openai_client import ask_openai
from app.models.agent_context_schema import AgentContext
import ast

def verified_articles(context: AgentContext) -> None:
    logger.info("---------------------------------Entering verified_articles function---------------------------------")        

    
    instruction = f"""
    You are an experienced news editor. Your task is to review the list of news articles that were selected by the selector agent.
    You must make sure they are relevant to the topic: {context.topic}.
    You will be given a list of objects which contains information about the news articles as follows:

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
    1. Given the topic {context.topic}, you will review content and title fields of each news article.
    2. After completing your analysis, you will determine if the articles are relevant to the main topic.
    3. Return a list containing the ids of the articles that are relevant to the topic. Do not add any other text.

    List of selected news articles by the selector agent:\n
    {context.selected_articles_content}

    """

    message = {"role": "system", "content": instruction}

    context.editor_history.append(message)

    # Appending selected articles to context
    response = ask_openai(context.editor_history, context)
    logger.info(f"Editor agent: The response is: {response}")

    # TODO: Create a function to convert the response to a list of boolean values
    response = ast.literal_eval(response)
    context.approved_articles_ids.extend(response)

    if len(context.approved_articles_ids) != 5:
        context.rejected_articles_ids = [article for article in context.selected_articles_ids if article not in response]
    logger.info(f"The number of approved articles: {len(context.approved_articles_ids)}")

    