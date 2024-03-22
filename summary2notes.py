from config import settings
from notion_client import Client
from datetime import datetime
import logging
import json
import os

TOKEN = settings.token
notion = Client(auth=TOKEN)

DATABASE_ID = settings.database_id


class BasePageBuilder:
    def __init__(self, summary_path: str, custom_name: str = None) -> None:
        with open(summary_path) as f:
            self.text_fields: dict = json.load(f)

        t_filename, _ = os.path.splitext(os.path.basename(summary_path))
        transcript_path = f"./transcripts/{t_filename}.txt"
        with open(transcript_path) as f:
            self.transcript = f.read()

        self.title = custom_name if custom_name else self.text_fields["title"]
        self.summary = self.text_fields["summary"]
        self.action_items = self.text_fields["action_items"]
        self.follow_up = self.text_fields["follow_up"]
        self.arguments = self.text_fields["arguments"]
        self.related_topics = self.text_fields["related_topics"]
        self.sentiment = self.text_fields["sentiment"]
        self.date = datetime.now().strftime("%Y-%m-%d")
        logging.info("PageBuilder initialized.")


class NotionPageBuilder(BasePageBuilder):
    """Class to create a Notion page from a summary file"""

    def create_page(self, database_id: str = DATABASE_ID) -> None:
        logging.info("Creating Notion page.")
        children = [
            self.create_heading_block("Summary"),
            self.create_paragraph_block(self.summary),
            self.create_heading_block("Action Items"),
            *[self.create_bullet_block(item) for item in self.action_items],
            self.create_heading_block("Follow Up"),
            *[self.create_bullet_block(item) for item in self.follow_up],
            self.create_heading_block("Arguments"),
            *[self.create_bullet_block(item) for item in self.arguments],
            self.create_heading_block("Related Topics"),
            *[self.create_bullet_block(item) for item in self.related_topics],
            self.create_heading_block("Sentiment"),
            self.create_paragraph_block(self.sentiment),
            self.create_heading_block("Date"),
            self.create_paragraph_block(self.date),
            self.create_heading_block("Transcript"),
            *self.create_paragraph_block_long(self.transcript),
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
            logging.info("Page created successfully.")
        except Exception as e:
            logging.error(f"Could not create Notion page. Error: {e}")

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

    @staticmethod
    def create_paragraph_block_long(text):
        blocks = []
        while text:
            block_text = text[:2000]
            text = text[2000:]
            blocks.append(
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": block_text},
                            }
                        ]
                    },
                }
            )
        return blocks


class MarkdownPageBuilder(BasePageBuilder):
    def __init__(self, summary_path: str, custom_name: str = None) -> None:
        super().__init__(summary_path, custom_name)
        self.filename = f"{self.title}.md"

    def create_page(self) -> None:
        logging.info("Creating Markdown page.")
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(f"# {self.text_fields['title']}\n\n")
            f.write("## Summary\n")
            f.write(f"- {self.summary}\n\n")
            f.write("## Action Items\n")
            for item in self.action_items:
                f.write(f"- {item}\n")
            f.write("\n## Follow Up\n")
            for item in self.follow_up:
                f.write(f"- {item}\n")
            f.write("\n## Arguments\n")
            for item in self.arguments:
                f.write(f"- {item}\n")
            f.write("\n## Related Topics\n")
            for item in self.related_topics:
                f.write(f"- {item}\n")
            f.write("\n## Sentiment\n")
            f.write(f"- {self.sentiment}\n\n")
            f.write("## Date\n")
            f.write(f"- {self.date}\n")
            f.write("\n## Transcript\n")
            f.write(f"- {self.transcript}\n")
        logging.info("Markdown page created successfully.")
