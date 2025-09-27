from types import CodeType
from app.services.logger import api_logger as logger
from newsapi import NewsApiClient
from dotenv import load_dotenv
from app.services.article_tools import get_article_text
from app.services.add_to_db import add_to_db
from app.services.test_db_has_items import test_db_has_items
from app.db.session import SessionLocal
from app.models.db_schema import NewsArticles
from sqlalchemy import text
import os
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_all_articles_from_db(from_date:str) -> list[dict]:
    """
    This function gets all articles from the database.
    """
    db = SessionLocal()
    try:
        return_articles = []
        articles = db.execute(text(f"SELECT * FROM news_articles where published_at >= '{from_date}'")).fetchall()
        for a in articles:
            return_articles.append(a._asdict())
        return return_articles
    except Exception as e:
        logger.error(f"Error getting articles from db: {e}")
        return []
    finally:
        db.close()

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
                    add_to_db(article)
        except Exception as e:
            logger.error(f"Error while fetching articles from News API and adding them to the database: {e}")
            return []
    
    return get_all_articles_from_db(from_date)
    
