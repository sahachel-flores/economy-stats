import requests
from app.database import get_db

db = get_db()

article = db.execute(text(f"SELECT * FROM news_articles where id == '{id}'")).fetchall()

# url = "https://api.stlouisfed.org/fred/category?category_id=125&api_key=73710b7590369eb9a43c051edcb204c4&file_type=json"

# response = requests.get(url)

# print(response.json())