# test/test_scraper.py
from app.services.logger import api_logger as logger
from app.news.news_api import get_news_articles_from_news_api

if __name__ == "__main__":
    logger.info("-----------------------------------starting test_article_scraper-----------------------------------")

    get_news_articles_from_news_api(query="US Economy", from_date="2025-06-16", to_date="2025-06-17")

    logger.info("-----------------------------------test_article_scraper completed-----------------------------------")

 