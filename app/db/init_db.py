from app.db.session import engine, Base
from app.models.news_articles import NewsArticles
from app.services.logger import api_logger as logger
# function to initialize the asyncdatabase
async def init_db():
    logger.info("2. Initializing the database.......")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
