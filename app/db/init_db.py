# app/db/init_db.py
from app.db.session import Base, engine
from app.models.db_schema import NewsArticles

def init_db():
    Base.metadata.create_all(bind=engine)
