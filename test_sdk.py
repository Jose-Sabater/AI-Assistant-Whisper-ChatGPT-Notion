from config import settings
import os
from notion_client import Client
from datetime import datetime

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

title = "This is a placeholder title"
summary = "this is my summary"
takeaway1 = "takeaway 1"
takeaway2 = "takeaway 2"
takeaway3 = "takeaway 3"
takeaway4 = "takeaway 4"
takeaway5 = "takeaway 5"


notion.pages.create(
    parent={"database_id": DATABASE_ID},
    # Title -------------------------------------------------------------------
    properties={
        "Title": {
            "title": [
                {
                    "text": {"content": title},
                    "plain_text": "second text",
                },
            ]
        }
    },
    # Summary -------------------------------------------------------------------
    children=[
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Summary"}}],
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": summary},
                    }
                ]
            },
        },
        # Takeaways -------------------------------------------------------------------
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Top 3 takeaways"}}],
            },
        },
        # Takeaway 1
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": takeaway1},
                    }
                ]
            },
        },
        # Takeaway 2
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": takeaway2},
                    }
                ]
            },
        },
        # Takeaway 3
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": takeaway3},
                    }
                ]
            },
        },
        # Takeaway 4
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": takeaway4},
                    }
                ]
            },
        },
        # Takeaway 5
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": takeaway5},
                    }
                ]
            },
        },
        # Date -------------------------------------------------------------------
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Date"}}],
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        },
                    }
                ]
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
