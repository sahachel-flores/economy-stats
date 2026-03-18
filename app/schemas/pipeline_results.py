from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

class PipelineRun(BaseModel):
    """
    SQLAlchemy ORM model for storing news pipeline run metadata.
    """

    __tablename__ = "pipeline_runs"

    topic: str
    from_date: str
    to_date: str
    status: str
    articles_processed: int
    approved_count: int
    approved_article_ids: list[int]