# test/test_scraper.py
from app.services.logger import api_logger as logger
from app.services.news_api_tools import get_news_articles_from_news_api
from app.models.agent_context_schema import AgentContext
from app.services.news_api_tools import get_article_text
from tests.init_db_session import SessionLocal

def test_get_news_articles_from_news_api():
    """
    Test the get_news_articles_from_news_api function.
    """
    context = AgentContext()
    db = SessionLocal()
    articles = get_news_articles_from_news_api(query="US Economy", from_date="2025-09-16", to_date="2025-09-17", context=context, db=db)
    assert len(articles) > 0
    db.close()
    logger.info(f"Number of articles: {len(articles)}")

def test_get_article_text():
    """
    Test the get_article_text function.
    """
    url = "https://www.cnn.com/2025/10/01/economy/adp-private-jobs-report-september"
    text = get_article_text(url)
    #logger.info(f"Text of article: {text}")
    assert text is not None and len(text) > 0 


if __name__ == "__main__":
    test_get_news_articles_from_news_api()
    test_get_article_text()
  