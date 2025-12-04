from pydantic import BaseModel, HttpUrl, Field
from datetime import date

class NewsRequest(BaseModel):
    topic: str = Field(..., description="The topic of the news")
    from_date: date = Field(..., description="The start date of the news")
    to_date: date = Field(..., description="The end date of the news")