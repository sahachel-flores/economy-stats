from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class PipelineRun(BaseModel):
    __tablename__ = "pipeline_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    from_date: Mapped[str] = mapped_column(String(50), nullable=False)
    to_date: Mapped[str] = mapped_column(String(50), nullable=False)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed")

    articles_processed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    approved_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    approved_article_ids: Mapped[str] = mapped_column(Text, nullable=True)
    #summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    #created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)