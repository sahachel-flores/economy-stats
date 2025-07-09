from app.scrapers.scraper import get_all_articles_for_today
from app.services.article_tools import scrape_article_text
from app.services.logger import api_logger as logger
# python -m app.test_scraper
if __name__ == "__main__":
    logger.info("-----------------------------------starting test_scraper-----------------------------------")
    articles = get_all_articles_for_today()
    logger.info(f"-----------------------------------scraped {len(articles)} articles-----------------------------------")
    logger.info("-----------------------------------scraper test_scraper completed-----------------------------------")

    logger.info(f"-----------------------------------article-----------------------------------")
    for article in articles:
        logger.info(article["title"])
    logger.info("-----------------------------------scraper test_scraper completed-----------------------------------")