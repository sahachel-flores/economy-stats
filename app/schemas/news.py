from pydantic import BaseModel, HttpUrl, Field
from datetime import date
from datetime import datetime
from typing import Optional


class NewsArticleResponse(BaseModel):
    id: int
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    url_to_image: Optional[str]
    published_at: datetime
    content: Optional[str]

    model_config = {"from_attributes": True}

class NewsRequest(BaseModel):
    topic: str = Field(..., description="The topic of the news")
    from_date: date = Field(..., description="The start date of the news")
    to_date: date = Field(..., description="The end date of the news")


class ArticleData(BaseModel):
    id: int | None = None
    author: Optional[str] = None
    title: str | None = None
    description: str | None = None
    url: str | None = None
    url_to_image: str | None = None
    published_at: datetime | None = None
    content: str | None = None

    model_config = {"from_attributes": True}