# run: python3 app/pipeline/news_pipeline.py
from app.models.agent_context_schema import AgentContext
from app.agents.selector_agent import select_articles
from app.services.logger import agent_logger as logger
from app.news.news_api import get_news_articles
from app.db.init_db import init_db
from app.agents.editor_agent import verified_articles

def run_news_pipeline() -> None:
    """
    Orchestrates the full news analysis pipeline:
    - Scrapes articles
    - Selects the top 5 relevant ones using agent
    """
    logger.info("Running news pipeline...")

    # Initialize the database
    init_db()

    # 1. Initialize agent context
    context = AgentContext()

    # 2. Get articles
    topic = "US Economy"
    context.topic = topic

    # Obtaining articles from the news api
    articles = get_news_articles(query=topic, from_date="2025-06-17", to_date="2025-06-17")
    logger.info(f"Number of articles: {len(articles)}\n\n")

    # Adding articles to the context
    context.articles = articles

    # Running the pipeline until we have 5 approved articles
    while context.attempt <= 2 and len(context.approved_articles_ids) < 5:
        # 3. Run article selector agent
        select_articles(articles, context=context)

        # 4. Run verifier agent
        verified_articles(context)
        context.attempt += 1
        

    # logger.info(f"We are out of attempts. Selected {len(context.selected_articles)} articles.")
    
run_news_pipeline()
