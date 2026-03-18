from sqlalchemy import Integer, String, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.session import Base


class PipelinesRuns(Base):
    __tablename__ = "pipeline_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    topic: Mapped[str] = mapped_column(String(128))
    from_date: Mapped[str] = mapped_column(String(50))
    to_date: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))
    articles_processed: Mapped[int] = mapped_column(Integer)
    approved_count: Mapped[int] = mapped_column(Integer)
    approved_article_ids: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # Todo: change to utc
    #summary = mapped_column(Text)
    #execution_time = mapped_column(Float)


