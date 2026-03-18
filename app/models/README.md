# Models (SQLAlchemy ORM)

**Purpose:** Database tables and persistence only.

- Use for `db.add()`, `db.execute(select(...))`, and all DB writes/reads.
- Do **not** use these as API response types; convert to Pydantic schemas via `app.serializers` or in the service layer.
