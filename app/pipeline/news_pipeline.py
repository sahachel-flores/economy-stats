# run: python3 app/pipeline/news_pipeline.py
from app.models.agent_context_schema import AgentContext
from app.agents.selector_agent import select_articles
from app.services.logger import agent_logger as logger
from app.services.news_api_tools import get_news_articles_from_news_api
from app.db.init_db import init_db
from app.agents.editor_agent import verified_articles
from app.agents.selector_agent_class import SelectorAgent
import asyncio

def run_news_pipeline() -> None:
    """
    Orchestrates the full news analysis pipeline:
    - Scrapes articles
    - Selects the top 5 relevant ones using agent
    """
    logger.info("Running news pipeline...")
    # initializing the agent context
    context = AgentContext()
    selector_agent = SelectorAgent(name="Selector Agent")
    context.control.topic = "US Economy"
    context.control.from_date = "2025-06-17"
    context.control.to_date = "2025-06-17"
    
    while context.should_continue():
        articles = get_news_articles_from_news_api(query=context.control.topic, from_date=context.control.from_date, to_date=context.control.to_date)
        context.article_flow.raw_articles.extend(articles)
        logger.info(f"Number of articles: {len(articles)}\n\n")
        
        # Running the selector agent
        selector_agent.execute(context)
        logger.info(f"Number of selected articles: {len(context.article_flow.selected_articles_ids)}\n\n")
        return 
        # 3. Run article selector agent
        #select_articles(articles, context=context)

        # 4. Run verifier agent
        #verified_articles(context)
        #context.attempt += 1
        

    # logger.info(f"We are out of attempts. Selected {len(context.selected_articles)} articles.")
    
run_news_pipeline()
