from fastapi import APIRouter, Depends, Request 
from app.pipeline.news_pipeline import run_news_pipeline
from app.core.dependencies import get_context
from app.core.run_context import RunContext
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

router = APIRouter(
    prefix='/homepage',
    tags=['homepage']
)



db_dependancy = Annotated[AsyncSession, Depends(get_db)]


@router.get("/{category}")
async def homepage(category: str, db: db_dependancy, context_dependency = Depends(get_context)):
    run_context = RunContext(context_dependency)
    run_news_pipeline(query=category, from_date="2025-10-01", to_date="2025-10-01", context=run_context.context, db=db)
    print(run_context.context.article_flow.approved_articles_ids)
    return run_context.context.article_flow.approved_articles_ids