from config import settings
import os
from notion_client import Client

TOKEN = settings.token

notion = Client(auth=TOKEN)
PAGE_ID = "e5a81e31-fb9c-421b-9288-2eeb57de01d8"

print(notion.databases.retrieve(database_id=PAGE_ID))
