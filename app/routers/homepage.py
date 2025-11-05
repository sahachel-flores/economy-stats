from fastapi import APIRouter, Depends, HTTPException, Request 
from app.pipeline.news_pipeline import run_news_pipeline
from app.core.dependecies import get_context
from app.core.run_context import RunContext
router = APIRouter(
    prefix='/homepage',
    tags=['homepage']
)

@router.get("/")
async def homepage(context_dependency = Depends(get_context)):
    run_context = RunContext(context_dependency)
    run_news_pipeline(query="economy", from_date="2025-10-01", to_date="2025-10-01", context=run_context)

    return [run_context.article_flow.approved_articles_content]