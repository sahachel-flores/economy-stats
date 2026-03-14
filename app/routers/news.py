from fastapi import APIRouter, HTTPException, Request, Depends
from app.schemas.news import NewsArticleResponse
from app.schemas.news_schema import News
from app.services.logger import api_logger
from app.db.session import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.db_tools import get_all_articles_from_db

router = APIRouter(
    prefix='/news',
    tags=['news']
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]

async def get_news(request: Request):
    api_logger.info("Getting news")
    return {"message": "Hello to Economy Stats AI"}

@router.get("/", response_model=list[NewsArticleResponse])
async def get_news(db: db_dependency):
    articles = await get_all_articles_from_db(db)
    return articles
