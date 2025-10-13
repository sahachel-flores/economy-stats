from app.db.session import SessionLocal
from app.models.db_schema import NewsArticles
from sqlalchemy import text
from app.services.logger import api_logger as logger

def add_articles_to_db(articles: list[dict], db: SessionLocal) -> bool:
    """
    This function adds an article to the database.
    """
    try:
        for article in articles:
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
            #logger.info(f"Adding article to the database: {article_db}")
            db.add(article_db)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"DB Error adding article to the database: {e}")
        db.rollback()
        return False
    finally:
        db.close()

   
def get_all_articles_from_db(db: SessionLocal, from_date:str = None) -> list[dict]:
    """
    This function gets all articles from the database.
    """
    
    try:
        return_articles = []
        if from_date:
            articles = db.execute(text(f"SELECT * FROM news_articles where published_at >= '{from_date}'")).fetchall()
        else:
            articles = db.execute(text(f"SELECT * FROM news_articles")).fetchall()

        if articles:
            for a in articles:
                return_articles.append(a._asdict())
        else:
            logger.info("No articles found in the database")
        return return_articles
    except Exception as e:
        logger.error(f"Error getting articles from db: {e}")
        return []
    finally:
        db.close()

def get_articles_using_ids_from_db(ids: list[int], db: SessionLocal) -> list[dict]:
    """
    This function gets the article from the database using the ids. It returns a list of dictionaries.
    """
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

def db_has_items(db: SessionLocal, from_date:str = None) -> bool:
    try:
        if from_date:
            return db.query(NewsArticles).filter(NewsArticles.published_at >= from_date).count() > 0
        else:
            return db.query(NewsArticles).count() > 0
    finally:
        db.close()

def remove_all_articles_from_db(db: SessionLocal) -> bool:
    """
    This function removes all articles from the database.
    """
    try:
        db.query(NewsArticles).delete()
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error removing all articles from the database: {e}")
        db.rollback()
        return False
    finally:
        db.close()




