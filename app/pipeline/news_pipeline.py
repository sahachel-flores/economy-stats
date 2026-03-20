# run: python3 app/pipeline/news_pipeline.py
from app.agents.agent_context_class import AgentContext
from app.services.logger import agent_logger as logger
from app.services.news_api_tools import get_news_articles_from_news_api
from app.agents.selector_agent_class import SelectorAgent
from app.agents.editor_agent_class import EditorAgent
from app.services.db_tools import remove_all_articles_from_db, add_articles_to_db, get_all_articles_from_db
from app.services.db_tools import db_has_items
from app.exceptions.pipeline_exceptions import FetchError, AgentExecutionError
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.sentiment_analysis_agent import SentimentAnalysisAgent

async def fetch_articles(context: AgentContext, db: AsyncSession) -> None:
    """
    Fetches articles from the database
    """
    try:
        if await db_has_items(db, from_date=context.control.from_date):
            context.article_flow.articles_from_db = await get_all_articles_from_db(db, from_date=context.control.from_date)
            logger.info(f"Articles already in the database: {len(context.article_flow.articles_from_db)}")
            return
        # getting the articles from the news api
        logger.info(f"Fetching articles from the news api...")
        raw_articles = get_news_articles_from_news_api(
            query=context.control.topic, 
            from_date=context.control.from_date, 
            to_date=context.control.to_date, 
            context=context)

        if len(raw_articles) == 0:
            raise FetchError("No articles returned from the news api")
        context.article_flow.raw_articles = raw_articles
        logger.info(f"Number of raw articles: {len(raw_articles)}")
        # adding the articles to the database
        await add_articles_to_db(raw_articles, db)
        articles_from_db = await get_all_articles_from_db(db, from_date=context.control.from_date)
        if len(articles_from_db) == 0:
            raise FetchError("Database returned no articles after insertion")
        context.article_flow.articles_from_db = articles_from_db
        logger.info(f"Number of articles in the database: {len(context.article_flow.articles_from_db)}")
    except Exception as e:
        raise FetchError(f"Failed fetching articles: {e}") from e


async def run_news_pipeline(context: AgentContext, db: AsyncSession) -> None:
    """
    Orchestrates the full news analysis pipeline:
    - Scrapes articles
    - Selects the top 5 relevant ones using agent
    """
    
    logger.info("Running news pipeline...")

    # initializing the agents
    selector_agent = SelectorAgent(name="Selector Agent")
    editor_agent = EditorAgent(name="Editor Agent")
    sentiment_analysis_agent = SentimentAnalysisAgent(name="Sentiment Analysis Agent")

    #logger.info(f"Articles to analyze: {context.article_flow.articles_from_db}")

    # running the pipeline
    try:
        # running the pipeline
        while context.should_continue():
            # getting the articles from the news api and storing them in the database
            if not await selector_agent.execute(context, db):
                raise Exception("Selector agent failed to execute")
            if not await editor_agent.execute(context, db):
                context.execution.attempt += 1
        sentiment_analysis_agent.execute(context)

    except Exception as e:
        raise Exception(f"Fatal error in the news pipeline: {e}")
    else:
        logger.info("News pipeline completed successfully!")
