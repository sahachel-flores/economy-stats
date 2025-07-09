# app/pipeline/news_pipeline.py
from app.agents.selector_agent import select_articles
from app.models.agent_context_schema import AgentContext
from app.services.logger import agent_logger as logger
from app.news.news_api import get_news_articles
from app.db.init_db import init_db

def run_news_pipeline() -> None:
    """
    Orchestrates the full news analysis pipeline:
    - Scrapes articles
    - Selects the top 5 relevant ones using agent
    """
    logger.info("Running news pipeline...")

    # Initialize the database
    init_db()

    #print("Running news pipeline...")
    # 1. Scrape articles900
    #articles = get_all_articles_for_today()
    articles = get_news_articles(query="US Economy", from_date="2025-06-17", to_date="2025-06-17")
    logger.info(f"Number of articles: {len(articles)}\n\n")
    #logger.info(f"Articles: {articles[2]}\n\n ")

    
    # 2. Initialize agent context
    context = AgentContext()
    
    
    while context.attempt <= 1 and len(context.selected_articles) < 5 and len(articles) > 0:
    #     # 3. Run article selector agent
        select_articles(articles, context=context)
        logger.info(f"............ breaking out of loop")
        break

    #     # 4. (Future) Run verifier agent
    #     # verified_articles = verifier_agent.verify(selected_articles, context)

    # logger.info(f"We are out of attempts. Selected {len(context.selected_articles)} articles.")
    
run_news_pipeline()