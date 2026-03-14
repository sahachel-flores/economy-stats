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