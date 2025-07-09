# app/scrapers/scraper.py

from datetime import datetime
from typing import List
import feedparser
from app.models.news_schema import News
#from services.news_utils import clean_summary
from app.services.logger import api_logger as logger
from newspaper import Article

NEWS_SOURCES = {
    "Economy": "https://news.google.com/rss/search?q=US+economy+when:1d&hl=en-US&gl=US&ceid=US:en",
    "Jobs": "https://news.google.com/rss/search?q=US+job+market+when:1d&hl=en-US&gl=US&ceid=US:en",
    "Housing": "https://news.google.com/rss/search?q=US+housing+market+when:1d&hl=en-US&gl=US&ceid=US:en",
    "Stocks": "https://news.google.com/rss/search?q=US+stock+market+when:1d&hl=en-US&gl=US&ceid=US:en",
}

def fetch_articles_from_feed(name: str, url: str, category: str) -> List[News]:
    try:
        logger.info(f"Fetching articles................")
        feed = feedparser.parse(url)
    except Exception as e:
        logger.error(f"Error parsing feed: {e}")
        return []
    
    articles = []

    # TODO: Add a check to see if the article is already in the database
    # If it is, skip it
    # If it is not, add it to the database
    logger.info(f"Storing all fetched articles................")
    i = 0
    for entry in feed.entries:
        # Some feeds don't include full metadata
        try:
            if i == 5:
                break
            article = Article(entry.link)
            article.download()
            article.parse()
            print(article)
            
            date = entry.published if hasattr(entry, "published") else datetime.now().isoformat()
            article = News(
                title=entry.title,
                description=entry.summary if hasattr(entry, "summary") else "",
                url=entry.link,
                source=name,
                category=category.lower(),
                date=date,
                author=getattr(entry, "author", "Unknown"),
                image="",  # Optional: if you later want to extract OG image
                summary="",
                relevant=True,
                semantic_score=0.0
            )
            articles.append(article.model_dump())
            i += 1
        except Exception as e:
            logger.warning(f"Skipping article due to error: {e}")
    return articles

def get_all_articles_for_today() -> List[dict]:
    """
    This function scrapes all the articles from the news sources for today and returns a list of News objects
    """
    all_articles = []
    logger.info(f"-----------------------------------starting scraper-----------------------------------")
    for source_name, feed_url in NEWS_SOURCES.items():
        # categorizing the source
        category = categorize_source(source_name) 
        logger.info(f"Scraping {source_name} for {category}")
        # getting the list of articles from the feed
        articles = fetch_articles_from_feed(source_name, feed_url, category) 
        logger.info(f"Fetched {len(articles)} articles from {source_name}")
        # adding the list of articles to all_articles
        all_articles.extend(articles) 
    logger.info(f"-----------------------------------ending scraper-----------------------------------")
    return all_articles


def categorize_source(source_name: str) -> str:
    """
    This function categorizes the source based on the source name
    """
    name = source_name.lower()
    if "economy" in name:
        return "economy"
    elif "job" in name:
        return "labor"
    elif "housing" in name:
        return "housing"
    elif "stock" in name:
        return "stocks"
    else:
        logger.error(f"Unknown source: {source_name}")
        return "misc"
