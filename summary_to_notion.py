from config import settings
import os
from notion_client import Client
from datetime import datetime
import json

TOKEN = settings.token
notion = Client(auth=TOKEN)

DATABASE_ID = settings.database_id

filename = "./summaries/data_utilization_out.json"


class NotionPageBuilder:
    def __init__(self, filename) -> None:
        with open(filename) as f:
            self.text_fields: dict = json.load(f)
        self.title = self.text_fields["title"]
        self.summary = self.text_fields["summary"]
        self.action_items = self.text_fields["action_items"]
        self.follow_up = self.text_fields["follow_up"]
        self.stories = self.text_fields["stories"]
        self.arguments = self.text_fields["arguments"]
        self.related_topics = self.text_fields["related_topics"]
        self.sentiment = self.text_fields["sentiment"]
        self.date = datetime.now().strftime("%Y-%m-%d")

    def create_page(self, database_id: str = DATABASE_ID) -> None:
        children = [
            self.create_heading_block("Summary"),
            self.create_paragraph_block(self.summary),
            self.create_heading_block("Action Items"),
            *[self.create_bullet_block(item) for item in self.action_items],
            self.create_heading_block("Follow Up"),
            *[self.create_bullet_block(item) for item in self.follow_up],
            self.create_heading_block("Stories"),
            *[self.create_bullet_block(item) for item in self.stories],
            self.create_heading_block("Arguments"),
            *[self.create_bullet_block(item) for item in self.arguments],
            self.create_heading_block("Related Topics"),
            *[self.create_bullet_block(item) for item in self.related_topics],
            self.create_heading_block("Sentiment"),
            self.create_paragraph_block(self.sentiment),
            self.create_heading_block("Date"),
            self.create_paragraph_block(self.date),
        ]
        try:
            notion.pages.create(
                parent={"database_id": database_id},
                # Title -------------------------------------------------------------------
                properties={
                    "Title": {
                        "title": [
                            {
                                "text": {"content": self.title},
                            }
                        ]
                    }
                },
                # Summary -------------------------------------------------------------------
                children=children,
            )
        except Exception as e:
            print(e)

    @staticmethod
    def create_bullet_block(item):
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": item},
                    }
                ]
            },
        }

    @staticmethod
    def create_heading_block(item):
        return {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": item},
                    }
                ]
            },
        }

    @staticmethod
    def create_paragraph_block(item):
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": item},
                    }
                ]
            },
        }
