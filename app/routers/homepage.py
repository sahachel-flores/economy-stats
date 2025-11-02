from fastapi import APIRouter, HTTPException, Request 
from app.services.logger import api_logger
from app.services.stats_services import get_economic_stats
from app.models.agent_context_schema import AgentContext
from app.pipeline.news_pipeline import run_news_pipeline


router = APIRouter(
    prefix='/homepage',
    tags=['homepage']
)

@router.get("/")
async def homepage():
    stats = get_economic_stats()
    context = AgentContext()
    run_news_pipeline(query="economy", from_date="2025-10-01", to_date="2025-10-01", context=context)

    return stats