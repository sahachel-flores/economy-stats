# run: python3 app/pipeline/news_pipeline.py
from app.models.agent_context_schema import AgentContext
from app.services.logger import agent_logger as logger
from app.services.news_api_tools import get_news_articles_from_news_api
from app.db.init_db import init_db
from app.agents.selector_agent_class import SelectorAgent
from app.agents.editor_agent_class import EditorAgent
from app.services.db_tools import remove_all_articles_from_db, add_articles_to_db, get_all_articles_from_db
from app.db.session import SessionLocal
from app.services.db_tools import db_has_items
import asyncio
from contextlib import contextmanager
from app.exceptions.pipeline_exceptions import FetchError, AgentExecutionError, PipelineError

# DB context manager
@contextmanager
def db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_articles(context, db):
    """
    Fetches articles from the database
    """
    try:
        if db_has_items(db, from_date=context.control.from_date):
            return
        # getting the articles from the news api
        logger.info(f"Fetching articles from the news api...")
        raw_articles = get_news_articles_from_news_api(
            query=context.control.topic, 
            from_date=context.control.from_date, 
            to_date=context.control.to_date, 
            context=context)

        if not raw_articles:
            raise FetchError("No articles returned from the news api")
        context.article_flow.raw_articles.append(raw_articles)
        # adding the articles to the database
        add_articles_to_db(raw_articles, db)
        articles_from_db = get_all_articles_from_db(db, from_date=context.control.from_date)
        if not articles_from_db:
            raise FetchError("Data returned no articles after insertion")
                  
        # adding the articles to the context
        context.article_flow.articles_from_db.append(articles_from_db[0])
        logger.info(f"Number of articles: {len(context.article_flow.articles_from_db)}\n\n")
    except Exception as e:
        raise FetchError(f"Failed fetching articles: {e}") from e

def run_agents(context, db, selector_agent, editor_agent):
    """
    Runs the selector and editor agents
    """
    try:
        if not selector_agent.execute(context, db):
            raise Exception("Selector agent failed to execute")
        if not editor_agent.execute(context, db):
            raise Exception("Editor agent failed to execute")

    except Exception as e:
        raise Exception(f"Agent execution failed: {e}")


def run_news_pipeline() -> None:
    """
    Orchestrates the full news analysis pipeline:
    - Scrapes articles
    - Selects the top 5 relevant ones using agent
    """
    
    logger.info("Running news pipeline...")
    #logger.info(f"items in db: {get_all_articles_from_db()}")
    # initializing the agent context
    context = AgentContext()
    context.control.topic = "US Economy"
    context.control.from_date = "2025-09-29"
    context.control.to_date = "2025-09-29"
    # initializing the agents
    selector_agent = SelectorAgent(name="Selector Agent")
    editor_agent = EditorAgent(name="Editor Agent")
    

    # running the pipeline
    try:
        with db_context() as db:
            # removing all articles from the database
            remove_all_articles_from_db(db)
            # running the pipeline
            while context.should_continue():
                # getting the articles from the news api and storing them in the database
                try:
                    fetch_articles(context, db)
                    run_agents(context, db, selector_agent, editor_agent)

                except Exception as e:
                    logger.error(f"Error while getting articles: {e}")
                    raise e
                finally:
                    context.control.attempt += 1

    except Exception as e:
        raise Exception(f"Fatal error in the news pipeline: {e}")
    else:
        logger.info("News pipeline completed successfully!")


run_news_pipeline()