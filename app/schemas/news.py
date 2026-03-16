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

class NewsApiArticle(BaseModel):
    author: str | None
    title: str
    description: str | None
    url: str
    urlToImage: str | None
    publishedAt: datetime
    content: str | None

class ArticleData(BaseModel):
    id: int
    author: Optional[str] = None
    title: str
    description: Optional[str] = None
    url: str
    url_to_image: Optional[str] = None
    published_at: datetime
    content: Optional[str] = None

    model_config = {"from_attributes": True}