import re
from fastapi import APIRouter, Depends, Query
from newspaper import article
from app.pipeline.news_pipeline import run_news_pipeline
from app.core.dependencies import get_context
from app.core.run_context import RunContext
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.agents.agent_context_class import AgentContext
from datetime import date
from app.schemas.news import NewsRequest
from app.services.db_tools import get_all_articles_from_db, ingest_api_news_to_db
from app.services.logger import agent_logger as logger
from app.services.db_tools import serialize_articles
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
    context_dep: agent_context_dependency):
    
    context = RunContext(context_dep)
    context.context.input.topic = request.topic
    context.context.input.from_date = request.from_date
    context.context.input.to_date = request.to_date

    #logger.info(f"topic: {context.context.control.topic} from_date: {context.context.control.from_date} to_date: {context.context.control.to_date}")

    # Fetching news api and storing result in the db
    await ingest_api_news_to_db(
        db,
        context.context,
        )
    
    # Getting articles from db
    articles = await get_all_articles_from_db(db, context.context.input.from_date)
    context.context.article_flow.articles_from_db = serialize_articles(articles)

    await run_news_pipeline(
        context=context.context, 
        db=db, 
        articles= articles
        )
    
    
    #print(context.context.article_flow.approved_articles_ids)
    #return context.context.article_flow.approved_articles_content