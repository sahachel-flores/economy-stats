from sqlalchemy import Column, Integer, String, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.session import Base

class NewsArticles(Base):
    __tablename__ = "news_articles_db"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    author: Mapped[str] = mapped_column(String(128))
    title: Mapped[str] = mapped_column(String(512))
    description: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(String(1024))
    url_to_image: Mapped[str] = mapped_column(String(1024))
    published_at: Mapped[datetime] = mapped_column(DateTime)
    content: Mapped[str] = mapped_column(Text)

    __table_args__ = (UniqueConstraint("url", name="uq_news_url"),)

