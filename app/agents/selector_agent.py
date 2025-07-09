# app/agents/selector_agent.py
from app.services.logger import api_logger as logger
from app.services.openai_client import ask_openai
from app.models.agent_context_schema import AgentContext


def select_articles(candidate_articles: list[dict], context: AgentContext) -> None:
    logger.info("---------------------------------Entering select_articles function---------------------------------")
    logger.info(f"------Attempt {context.attempt}: Selecting from {len(candidate_articles)} candidates.------")
        

    
    if context.attempt == 1:
        logger.info("First attempt")
        prompt = f"""
        You are an expert news analyst assistant. Your task is to select the five most relevant articles for a news website 
        specializing in the U.S. economy.
        You will be given a list of objects which contains information about the news article:

        Use the following criteria to select the articles:
        1. You will loop through the list of objects and analyze the content field of the article.
        2. After completing your analysis, you will select the five most relevant articles.
        2. You can only select an article once.
        3. If one or more fields are empty, you should not select it.
        4. Return a list containing the ids of the five selected articles. Do not add any other text.

        Here are the list of news article:\n
        {candidate_articles}
        """

        messages = [
            {"role": "system", "content": prompt}
        ]
    else:
        logger.info(f"One or more articles were rejected. Attempt {context.attempt}")
        logger.info(f"Selected articles: {len(context.selected_articles)} and rejected articles: {len(context.rejected_articles)}")
        number_article_select = len(context.selected_articles) - len(context.rejected_articles)
        messages = context.feedback_log + [
            {"role": f"system", "content": "Please reselect {number_article_select} news articles considering the feedback."}
        ]

    
    # Appending selected articles to context
    ask_openai(messages, context)
    logger.info(f"The number of selected articles are: {len(context.selected_articles)}\n")
    logger.info(f"The selected articles are: \n{context.selected_articles}")
    context.attempt += 1
    