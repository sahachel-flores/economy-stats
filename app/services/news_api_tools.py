from app.services.logger import api_logger as logger
from newsapi import NewsApiClient
from dotenv import load_dotenv
import newspaper
from app.models.agent_context_schema import AgentContext
import os
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")



# TODO: return news articles using the range provided by the user. I currently uses the from_date to get all articles from the database.
def get_news_articles_from_news_api(query:str, from_date:str, to_date:str, context: AgentContext) -> list[dict]:
    """
    This function gets the news articles from the News API.
    """

    try:

        logger.info("-----------------------------DB is empty, getting all articles from News API---------------------------")

        try:
            # Initialize the News API client
            newsapi = NewsApiClient(api_key=NEWS_API_KEY)

            # Get all articles from the News API
            all_articles = newsapi.get_everything(q=query,
                                        from_param=from_date,
                                        to=to_date,
                                        language='en',
                                        sort_by='relevancy',
                                        page_size=30
                                        )
        except Exception as e:
            logger.error(f"Error while fetching articles from News API: {e}")
            return []

        context.control.obtained_articles_from_news_api = len(all_articles["articles"])
        if context.control.obtained_articles_from_news_api > 0 and context.control.obtained_articles_from_news_api < context.control.target_articles:
            logger.info(f"The number of articles obtained from News API is less than the target articles. Setting the target articles to {context.control.obtained_articles_from_news_api}")
            context.control.target_articles = context.control.obtained_articles_from_news_api
        elif context.control.obtained_articles_from_news_api == 0:
            logger.info(f"The number of articles obtained from News API is 0.")
            context.control.target_articles = 0
            return []
        return all_articles["articles"]
    except Exception as e:
        logger.error(f"Error while fetching articles from News API and adding them to the context: {e}")
        return []
 

def get_article_text(url: str | None) -> str:
    """
    This function gets the text of the article from the url.
    """
    try:
        # Initialize the article object

        article = newspaper.article(url, language='en')
        article.download()
        article.parse()

        # Return the text of the article
        return article.text
    except Exception as e:
        logger.error(f"Error parsing text of article with url: {url}: {e}")
        return None

def get_article_summary(url: str | None) -> str:
    """
    This function gets the summary of the article from the url.
    """
    try:
        # Initialize the article object
        article = newspaper.article(url, language='en')
        article.download()
        article.parse()

        # Return the summary of the article
        if article.summary:
            return article.summary
        else:
            return None
    except Exception as e:
        logger.error(f"Error parsing summary of article with url: {url}: {e}")
        return None