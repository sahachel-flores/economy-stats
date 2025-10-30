from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class NewsIn(BaseModel):
    author: str
    title: str
    description: str
    url: HttpUrl
    url_to_image: HttpUrl
    published_at: str
    content: str

class NewsOut(BaseModel):
    id: int
    author: str
    title: str
    description: str
    url: HttpUrl
    url_to_image: HttpUrl
    published_at: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True