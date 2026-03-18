"""
Pydantic schemas for pipeline run data.

Use these for API request/response and validation only.
Do not use for database persistence — use app.models.pipeline_runs.PipelinesRuns instead.
"""

from pydantic import BaseModel


class PipelineRunSchema(BaseModel):
    """
    DTO for a single pipeline run. Use for API responses and validation.
    For DB persistence use app.models.pipeline_runs.PipelinesRuns.
    """

    id: int | None = None
    topic: str
    from_date: str
    to_date: str
    status: str
    articles_processed: int
    approved_count: int
    approved_article_ids: list[int]

    model_config = {"from_attributes": True}
