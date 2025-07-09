# app/services/article_tools.py

from newspaper import Article
from app.services.logger import api_logger as logger
from app.db.session import SessionLocal
from app.models.db_schema import NewsArticles



def get_article_text(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logger.error(f"Error parsing article {url}: {e}")
        return None

def get_article_summary(url: str) -> str:
    article = Article(url)
    article.download()
    article.parse()
    return article.summary

def get_articles_from_ids(ids: list[str]) -> list[dict]:
   
    try:
        db = SessionLocal()
        articles = []
        logger.info(f"The ids are: {ids}")
        for id in ids:
            try:
                logger.info(f"The id is: {id}")
                article = db.query(NewsArticles).filter(NewsArticles.id == id).first()
                logger.info(f"The article is: \n{article}")
            except Exception as e:
                logger.error(f"Error getting article {id}: {e}")
                continue
            articles.append(article._asdict())
        return articles
    finally:
        db.close()