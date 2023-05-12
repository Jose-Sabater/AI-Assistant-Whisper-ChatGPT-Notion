from config import settings
import os
from notion_client import Client

TOKEN = settings.token
notion = Client(auth=TOKEN)

DATABASE_ID = settings.database_id


# Retrieve database info
# databases = notion.databases.retrieve(database_id=DATABASE_ID)
# print(databases["last_edited_time"])

# -------------------------------------------------------------------------------
# create
# notion.pages.create(
#     parent={"database_id": DATABASE_ID},
#     properties={
#         "Title": {
#             "title": [
#                 {
#                     "text": {"content": "This is the first test"},
#                     "plain_text": "second text",
#                 }
#             ]
#         },
#     },
# )

notion.pages.create(
    parent={"database_id": DATABASE_ID},
    properties={
        "Title": {
            "title": [
                {
                    "text": {"content": "This is the first test"},
                    "plain_text": "second text",
                },
            ]
        }
    },
    children=[
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Heading 2"}}],
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "## Paragraph"}}]
            },
        },
    ],
)


# -------------------------------------------------------------------------------
# Retrieve pages and update
# pages = notion.databases.query(database_id=DATABASE_ID)
# for page in pages["results"]:
#     print(page["properties"]["Title"]["title"][0]["plain_text"])
#     if (
#         page["properties"]["Title"]["title"][0]["plain_text"]
#         == "This is the first test"
#     ):
#         notion.pages.update(
#             page_id=page["id"],
#             properties={
#                 "Title": {
#                     "title": [
#                         {
#                             "text": {"content": "This is the second test"},
#                             "plain_text": "second text",
#                         }
#                     ]
#                 },
#             },
#         )
