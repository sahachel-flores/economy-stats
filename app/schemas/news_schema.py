from pydantic import BaseModel

class News(BaseModel):
    title: str
    description: str
    url: str
    source: str
    category: str
    date: str
    author: str
    image: str
    summary: str
    relevant: bool
    semantic_score: float
