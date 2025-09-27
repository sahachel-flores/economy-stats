from app.services.logger import api_logger as logger
from newsapi import NewsApiClient
from dotenv import load_dotenv
from app.services.db_tools import add_article_to_db
from app.services.db_tools import test_db_has_items
from app.services.db_tools import get_all_articles_from_db
from newspaper import Article
import os
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")



# TODO: return news articles using the range provided by the user. I currently uses the from_date to get all articles from the database.
def get_news_articles_from_news_api(query:str, from_date:str, to_date:str) -> list[dict]:
    """
    This function gets the news articles from the News API and adds them to the database.
    """

    if not test_db_has_items():
        logger.info(f"The database is empty. Adding all articles to the database.")

        try:

            logger.info("-----------------------------DB is empty, getting all articles from News API---------------------------")

            # Initialize the News API client
            newsapi = NewsApiClient(api_key=NEWS_API_KEY)

            # Get all articles from the News API
            all_articles = newsapi.get_everything(q=query,
                                        from_param=from_date,
                                        to=to_date,
                                        language='en',
                                        sort_by='relevancy',
                                        )
        

            # Add all candidate articles to the database
            for article in all_articles["articles"]:
                # Get the content of the article by scraping the url using the newspaper library
                content = get_article_text(article["url"])
                if content:
                    article["content"] = content
                    add_article_to_db(article)
        except Exception as e:
            logger.error(f"Error while fetching articles from News API and adding them to the database: {e}")
            return []
    
    return get_all_articles_from_db(from_date)
    

def get_article_text(url: str) -> str:
    """
    This function gets the text of the article from the url.
    """
    try:
        # Initialize the article object
        article = Article(url)

        # Download and parse the article
        article.download()
        article.parse()

        # Return the text of the article
        return article.text
    except Exception as e:
        logger.error(f"Error parsing article {url}: {e}")
        return None

def get_article_summary(url: str) -> str:
    """
    This function gets the summary of the article from the url.
    """
    try:
        # Initialize the article object
        article = Article(url)

        # Download and parse the article
        article.download()
        article.parse()

        # Return the summary of the article
        return article.summary
    except Exception as e:
        logger.error(f"Error parsing url {url}: {e}")
        return None