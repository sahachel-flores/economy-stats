import requests

url = "https://api.stlouisfed.org/fred/category?category_id=125&api_key=73710b7590369eb9a43c051edcb204c4&file_type=json"

response = requests.get(url)

print(response.json())