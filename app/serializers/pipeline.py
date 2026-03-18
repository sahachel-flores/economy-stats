"""
Convert pipeline ORM rows to API schemas.
Keeps schema/model separation: only this module imports both.
"""

import json
from app.models.pipeline_runs import PipelinesRuns
from app.schemas.pipeline_results import PipelineRunSchema


def pipeline_run_orm_to_schema(row: PipelinesRuns) -> PipelineRunSchema:
    """Build a PipelineRunSchema from a PipelinesRuns ORM instance."""
    ids = row.approved_article_ids
    if isinstance(ids, str):
        ids = json.loads(ids) if ids else []
    return PipelineRunSchema(
        id=row.id,
        topic=row.topic,
        from_date=row.from_date,
        to_date=row.to_date,
        status=row.status,
        articles_processed=row.articles_processed,
        approved_count=row.approved_count,
        approved_article_ids=ids,
    )
