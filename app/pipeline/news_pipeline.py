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
    # initializing the agents
    selector_agent = SelectorAgent(name="Selector Agent")
    editor_agent = EditorAgent(name="Editor Agent")
    # setting the control parameters
    context.control.topic = "US Economy"
    context.control.from_date = "2025-09-29"
    context.control.to_date = "2025-09-29"
    # initializing the database session
    db = SessionLocal()
    # running the pipeline

    remove_all_articles_from_db(db)
    while context.should_continue():

        try:
            # getting the articles from the news api
            if not db_has_items(db, from_date=context.control.from_date):
                raw_articles = get_news_articles_from_news_api(query=context.control.topic, from_date=context.control.from_date, to_date=context.control.to_date, context=context)
                if raw_articles:
                    # adding the articles to the database
                    add_articles_to_db(raw_articles, db)
                else:
                    logger.error("No articles found. Exiting the pipeline.")
                    return
            articles = get_all_articles_from_db(db, from_date=context.control.from_date)
        except Exception as e:
            logger.error(f"Error getting articles from the database: {e}")
            return

        # verifying that the database returns
        if len(articles) > 0:
            context.article_flow.raw_articles.append(raw_articles)
            logger.info(f"Number of articles: {len(articles)}\n\n")
        else:
            # TODO: when UI is implemented, we should show a message to the user that no articles were found for the given topic and date range
            logger.info("No articles found. Exiting the pipeline.")
            return
        
        # Running the selector agent
        if selector_agent.execute(context, db):
            logger.info("Selector agent executed successfully")
            
        else:
            logger.error("Selector agent failed to execute")
            return
        
        # Run editor agent
        if editor_agent.execute(context, db):
            logger.info("Editor agent executed successfully")
            context.control.attempt += 1
        else:
            logger.error("Editor agent failed to execute")
            return
        # remove all articles from the database
        #remove_all_articles_from_db()
        return
        
        # Run verifier agent
        #verified_articles(context)
        #context.attempt += 1
        

    # logger.info(f"We are out of attempts. Selected {len(context.selected_articles)} articles.")
    
run_news_pipeline()
