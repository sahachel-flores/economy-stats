# app/services/article_tools.py
from app.services.logger import api_logger as logger
from app.db.session import SessionLocal
from app.models.db_schema import NewsArticles



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
            article = db.query(NewsArticles).filter(NewsArticles.id == id).first()
            if article:
                article_dict = {
                    "id": article.id,
                    "author": article.author,
                    "title": article.title,
                    "description": article.description,
                    "url": article.url,
                    "url_to_image": article.url_to_image,
                    "published_at": article.published_at,
                    "content": article.content
                }
                articles.append(article_dict)
            else:
                logger.error(f"Article with id {id} not found")
                return []

        # Return the list of articles
        return articles
    except Exception as e:
        logger.error(f"Error getting articles from ids: {e}")
        return []
    finally:
        # Close the database session
        db.close()