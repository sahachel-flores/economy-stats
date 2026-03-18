# Schemas (Pydantic)

**Purpose:** Request/response validation and DTOs. No database persistence.

- Use for API bodies, query params, and any data validation.
- Do **not** import SQLAlchemy or `app.models` here.
- To expose DB entities in the API, convert in `app.serializers` or in the service layer.
