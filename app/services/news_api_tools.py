from app.services.logger import api_logger as logger
from newsapi import NewsApiClient
from dotenv import load_dotenv
import newspaper
from app.agents.agent_context_class import AgentContext
import os
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")



# TODO: return news articles using the range provided by the user. I currently uses the from_date to get all articles from the database.
def get_news_articles_from_news_api(query:str, from_date:str, to_date:str, context: AgentContext) -> list[dict]:
    """
    This function gets the news articles from the News API.
    """

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
        num_fetched_articles = len(all_articles["articles"])
        if num_fetched_articles < context.control.min_articles_fetch:
            logger.info(f"The number of articles fetched by News API is less than the minimum number of articles required.")
            raise Exception(f"Number of fetched news articles is {num_fetched_articles} which less than the minumum required ({context.control.min_articles_fetch})")
        
        context.article_flow.raw_articles.append(all_articles["articles"])
        logger.info(f"Number of raw articles: {len(all_articles["articles"])}")
        
        return all_articles["articles"]

    except Exception as e:
        logger.error(f"Error while fetching articles from News API: {e}")
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