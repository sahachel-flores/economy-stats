from app.services.logger import api_logger as logger
from app.news.news_api import get_google_news_articles

if __name__ == "__main__":
    logger.info("-----------------------------------starting test_article_scraper-----------------------------------")

    get_google_news_articles()

    logger.info("-----------------------------------test_article_scraper completed-----------------------------------")

 