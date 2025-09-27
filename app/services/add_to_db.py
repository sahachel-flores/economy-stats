from app.db.session import SessionLocal
from app.models.db_schema import NewsArticles
from app.services.logger import agent_logger as logger

def add_to_db(article: dict) -> None:
    """
    This function adds an article to the database.
    """
    # Initialize the database session
    db = SessionLocal()

    try:
        # Create article object with proper field mapping
        article_db = NewsArticles(
            author=article["author"],
            title=article["title"],
            description=article["description"],
            url=article["url"],
            url_to_image=article["urlToImage"],
            published_at=article["publishedAt"],
            content=article["content"],
        )

        # Add the article to the database
        logger.info(f"Adding article to the database: {article_db}")
        db.add(article_db)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"DB Error adding article to the database: {e}")
        db.rollback()
        return False
    finally:
        db.close()

   


