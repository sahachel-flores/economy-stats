from app.db.session import SessionLocal
from app.models.db_schema import NewsArticles

"""
This function tests if the database has any items.
If it does, it returns True, otherwise it returns False.s
"""
def test_db_has_items() -> bool:
    db = SessionLocal()
    try:
        return db.query(NewsArticles).count() > 0
    finally:
        db.close()




