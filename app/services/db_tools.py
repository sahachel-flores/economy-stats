from logging import Logger
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.agents.agent_context_class import AgentContext
from app.models.news_articles import NewsArticles
from sqlalchemy import text
from app.services.logger import api_logger as logger
from sqlalchemy import select, delete
from datetime import datetime
from app.services.news_api_tools import get_news_articles_from_news_api


async def add_articles_to_db(articles: list[dict], db: AsyncSession) -> None:
    """
    This function adds articles to the database.
    """

    required_fields = ["author", "title", "description", "url", "urlToImage", "publishedAt", "content"]
    async with db.begin():
        for article in articles:
            
            if not all(article.get(field) for field in required_fields):
                logger.warning(f"Skipping article due to missing fields")
                continue
            try:
                # Create article object with proper field mapping
                published_at_dt = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
            

            except Exception:
                logger.warning("Skipping article due to invalid publishedAt")
                continue
                
            stmt = select(NewsArticles.id).where(NewsArticles.url == article['url'])
            result = await db.execute(stmt)
            
            # Check to avoid adding duplicate articles 
            if result.scalar_one_or_none():
                logger.warning(f"skipping duplicate article url {article['url']}")
                continue
            
            article_db = NewsArticles(
                    author=article["author"],
                    title=article["title"],
                    description=article["description"],
                    url=article["url"],
                    url_to_image=article["urlToImage"],
                    published_at=published_at_dt,
                    content=article["content"],
            )

            # Add the article to the database
            db.add(article_db)
        

   
async def get_all_articles_from_db(db: AsyncSession, from_date:str | None) -> list[NewsArticles]:
    """
    This function gets all articles from the database.
    """
    
    try:
        # Create a select statement to select all articles
        stmt = select(NewsArticles)

        # Filter the articles by the published date if provided
        if from_date:
            stmt = stmt.where(NewsArticles.published_at >= from_date)
        result = await db.execute(stmt)    # await the execution
        articles = result.scalars().all()  # get list of articles

        return articles
    except Exception as e:
        logger.error(f"Error getting articles from db: {e}")
        return []
       

async def get_articles_using_ids_from_db(ids: list[int], db: AsyncSession) -> list[dict]:
    """
    This function gets the article from the database using the ids. It returns a list of dictionaries.
    """
    logger.info(f"Fetching articles from ids: {ids}")
    try:
        return_articles = []

        # Create a select statement to select the articles by the ids
        stmt = select(NewsArticles).where(NewsArticles.id.in_(ids))
        result = await db.execute(stmt)
        articles = result.scalars().all()

        return_articles = [
            {
                "id": a.id,
                "author": a.author,
                "title": a.title,
                "description": a.description,
                "url": a.url,
                "url_to_image": a.url_to_image,
                "published_at": a.published_at,
                "content": a.content
            } for a in articles
        ]
        return return_articles

    except Exception as e:
        logger.error(f"Error getting articles from ids: {e}")
        return []
        

async def db_has_items(db: AsyncSession, from_date:str = None) -> bool:
    """
    This function checks if the database has items.
    """
    try:
        stmt = select(NewsArticles)
        if from_date:
            parsed_from_date = datetime.fromisoformat(from_date)
            stmt = stmt.filter(NewsArticles.published_at >= parsed_from_date)
        result = await db.execute(stmt)
        return True if result.scalars().all() else False
    except Exception as e:
        await db.rollback()
        logger.error(f"Error checking if the database has items: {e}")
        return False
        

async def remove_all_articles_from_db(db: AsyncSession) -> bool:
    """
    This function removes all articles from the database.
    """
    try:
        stmt = delete(NewsArticles)
        await db.execute(stmt)
        await db.commit()
        logger.info("All articles removed from the database")
        return True
    except Exception as e:
        await db.rollback()
        logger.error(f"Error removing all articles from the database: {e}")
        return False
        



async def ingest_api_news_to_db(db: AsyncSession, context: AgentContext) -> None:
    """
    This function fetches the news_api and stores the result in the database.
    """
    articles = get_news_articles_from_news_api(
        query=context.control.topic,
        from_date=context.control.from_date,
        to_date=context.control.to_date,
        context=context,
    )

    await add_articles_to_db(articles, db)

def serialize_articles(articles):
    return [
        {
            "id": a.id,
            "author": a.author,
            "title": a.title,
            "description": a.description,
            "url": a.url,
            "url_to_image": a.url_to_image,
            "published_at": a.published_at,
            "content": a.content,
        }
        for a in articles
]