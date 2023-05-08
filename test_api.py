import requests
import os
from config import settings

TOKEN = settings.token
NOTION_VERSION = "2022-06-28"

path = "b3c2bc9515a24804b1a9eb63474663af"
# bearer token in headers

headers = {
    "accept": "application/json",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}

payload = {"page_size": 100}
# result = requests.get(f"https://api.notion.com/v1/users", headers=headers)
result = requests.post(f"https://api.notion.com/v1/search", headers=headers)
print(result.status_code)
print(result.json())
