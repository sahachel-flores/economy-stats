# app/services/article_tools.py

from newspaper import Article
from app.services.logger import api_logger as logger
from app.db.session import get_db
from app.db.session import SessionLocal
from app.models.db_schema import NewsArticles
from sqlalchemy import text


def get_article_text(url: str) -> str:
    """
    This function gets the text of the article from the url.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logger.error(f"Error parsing article {url}: {e}")
        return None

def get_article_summary(url: str) -> str:
    """
    This function gets the summary of the article from the url.
    """
    article = Article(url)
    article.download()
    article.parse()
    return article.summary

def get_articles_from_ids(ids: list[str]) -> list[dict]:
    """
    This function gets the article from the database using the ids.
    """
   
    try:
        with SessionLocal() as db:
            articles = []
            logger.info(f"The ids are: {ids}")
            for id in ids:
                try:
                    logger.info(f"The id is: {id}")
                    #article = db.query(NewsArticles).filter(NewsArticles.id == id).first()
                    article = db.execute(text(f"SELECT * FROM news_articles where id == '{id}'")).fetchall()
                    article = article[0]._asdict()
                except Exception as e:
                    logger.error(f"Error fetching one of the id:{id}: {e}")
                    continue
                articles.append(article)
        return articles
    except Exception as e:
        logger.error(f"DB Error getting articles from ids: {e}")
        return []