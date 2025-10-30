from fastapi import APIRouter, HTTPException, Request 
from app.services.logger import api_logger
from app.services.stats_services import get_economic_stats
from app.services.news_api_tools import get_news_articles_from_news_api
from app.models.agent_context_schema import AgentContext

router = APIRouter(
    prefix='/homepage',
    tags=['homepage']
)

@router.get("/")
async def homepage():
    stats = get_economic_stats()
    context = AgentContext()
    news = get_news_articles_from_news_api(query="economy", from_date="2025-01-01", to_date="2025-01-01", context=context)
    