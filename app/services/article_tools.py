# app/services/article_tools.py

from newspaper import Article
from app.services.logger import api_logger as logger
from app.db.session import SessionLocal
from app.models.db_schema import NewsArticles
from sqlalchemy import text



def get_articles_from_ids(ids: list[int]) -> list[dict]:
    """
    This function gets the article from the database using the ids. It returns a list of dictionaries.
    """
    # Initialize the database session
    db = SessionLocal()
    try:
        # Article list to store the articles
        articles = []
        logger.info(f"Fetching articles from ids: {ids}")

        # Iterate over the ids
        for id in ids:
            # Get the article from the database
            #article = db.query(NewsArticles).filter(NewsArticles.id == id).first()
            article = db.execute(text(f"SELECT * FROM news_articles where id == '{id}'")).fetchall()
            article = article[0]._asdict()

            # If the article is found, add it to the list
            if article:
                articles.append(article)

        # Return the list of articles
        return articles
    except Exception as e:
        logger.error(f"Error getting articles from ids: {e}")
        return []
    finally:
        # Close the database session
        db.close()