# test/test_scraper.py
from app.services.logger import api_logger as logger
from app.services.news_api_tools import get_news_articles_from_news_api
from app.models.agent_context_schema import AgentContext
from app.services.news_api_tools import get_article_text
from app.services.db_tools import add_articles_to_db
from app.models.db_schema import NewsArticles

def test_get_news_articles_from_news_api():
    """
    Test the get_news_articles_from_news_api function.
    """
    context = AgentContext()

    articles = get_news_articles_from_news_api(query="US Economy", from_date="2025-09-26", to_date="2025-09-27", context=context)
    assert len(articles) == len(articles)



def test_get_article_text():
    """
    Test the get_article_text function.
    """
    url = "https://www.cnn.com/2025/10/01/economy/adp-private-jobs-report-september"
    text = get_article_text(url)
    #logger.info(f"Text of article: {text}")
    assert text is not None and len(text) > 0 

