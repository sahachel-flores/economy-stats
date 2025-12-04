from fastapi import APIRouter, Depends, Query
from app.pipeline.news_pipeline import run_news_pipeline
from app.core.dependencies import get_context
from app.core.run_context import RunContext
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.agents.agent_context_class import AgentContext
from datetime import date
from app.schemas.news import NewsRequest

router = APIRouter(
    prefix='/homepage',
    tags=['homepage']
)

# Dependencies injections
db_dependency = Annotated[AsyncSession, Depends(get_db)]
agent_context_dependency = Annotated[AgentContext, Depends(get_context)]


@router.post("/")
async def homepage(
    request: NewsRequest,
    db: db_dependency, 
    context: agent_context_dependency):
    
    run_context = RunContext(context)
    await run_news_pipeline(topic=request.topic, from_date=request.from_date, to_date=request.to_date, context=run_context.context, db=db)
    print(run_context.context.article_flow.approved_articles_ids)
    return run_context.context.article_flow.approved_articles_content