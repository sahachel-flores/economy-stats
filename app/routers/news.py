from fastapi import APIRouter, HTTPException, Request 
from app.models.news_schema import News
from app.services.logger import api_logger
from app.db.session import SessionLocal

router = APIRouter(
    prefix='/news',
    tags=['news']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def get_news(request: Request):
    api_logger.info("Getting news")
    return {"message": "Hello to Economy Stats AI"}

@router.get("/{category}")
async def get_news(category: str):
    if category not in CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")

    
