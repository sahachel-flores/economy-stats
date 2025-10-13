from sqlalchemy import Column, Integer, String, DateTime
from app.db.session import Base

class NewsArticles(Base):
    __tablename__ = "news_articles"
    id = Column(Integer, primary_key=True, index=True)
    author = Column(String)
    title = Column(String)
    description = Column(String)
    url = Column(String)
    url_to_image = Column(String)
    published_at = Column(String)
    content = Column(String)
class TestData(Base):
    __tablename__ = "test_news_articles"
    id = Column(Integer, primary_key=True, index=True)
    author = Column(String)
    title = Column(String)
    description = Column(String)
    url = Column(String)
    url_to_image = Column(String)
    published_at = Column(String)
    content = Column(String)