from app.db.session import SessionLocal
from app.models.db_schema import NewsArticles
from app.services.logger import agent_logger as logger

def add_to_db(article: dict) -> None:
    # Create a new article object
    article_db = NewsArticles(
        author=article["author"],
        title=article["title"],
        description=article["description"],
        url=article["url"],
        url_to_image=article["urlToImage"],
        published_at=article["publishedAt"],
        content=article["content"],
    )

    # Initialize the database session
    db = SessionLocal()
    try:
        # Add the article to the database
        logger.info(f"Adding article to the database: {article_db}")
        db.add(article_db)
        db.commit()
    finally:
        logger.info(f"Closing the database session")
        db.close()

   


