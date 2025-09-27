import requests
from app.database import get_db

db = get_db()

article = db.execute(text(f"SELECT * FROM news_articles where id == '{id}'")).fetchall()


