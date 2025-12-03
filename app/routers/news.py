from fastapi import APIRouter, HTTPException, Request 
from app.schemas.news_schema import News
from app.services.logger import api_logger
from app.db.session import get_db

router = APIRouter(
    prefix='/news',
    tags=['news']
)


@router.get("/")
async def get_news(request: Request):
    api_logger.info("Getting news")
    return {"message": "Hello to Economy Stats AI"}

@router.get("/{category}")
async def get_news(category: str):
    CATEGORIES = ['us economy', 'housing', 'stock', 'labor']
    if category not in CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")

    
