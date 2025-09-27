# app/services/article_tools.py

from newspaper import Article
from app.services.logger import api_logger as logger
from app.db.session import SessionLocal
from app.models.db_schema import NewsArticles
from sqlalchemy import text


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

def get_articles_from_ids(ids: list[str]) -> list[dict]:
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