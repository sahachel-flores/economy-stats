from pydantic import BaseModel

class SelectedArticleIds(BaseModel):
    article_ids: list[int]

class ApprovedArticleIds(BaseModel):
    article_ids: list[int]

class SentimentAnalysisResult(BaseModel):
    id: int
    rating: int
    sentiment: str