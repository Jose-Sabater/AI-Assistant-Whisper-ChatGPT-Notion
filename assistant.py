"""
Class that creates a Notion page out of a video file, using the following steps:
Steps:
1. Convert video to audio
2. Transcribe audio to text
3. Summarize text
4. Create Notion page

To run just call the make_notes method
"""

import os
import logging
from video2audio import extract_audio
from audio2text import transcribe
from text2summary import OpenAISummarizer
from summary2notes import NotionPageBuilder, MarkdownPageBuilder
from utils.errors import NotionPageError, UnsupportedFormatError, MarkdownPageError


class NotesAssistant:
    def __init__(self, media_path: str, output_format: str = "Notion"):
        if not media_path:
            raise ValueError("media_path is required")

        self.media_path = media_path
        self.filename, self.extension = os.path.splitext(os.path.basename(media_path))
        self.custom_name = None
        self.output_format = output_format  # Notion or Markdown

        # Initialize paths for each step
        self.audio_file_path = None
        self.transcript_path = None
        self.summary_path = None

    def make_notes(self, custom_name: str = None):
        if custom_name:
            self.custom_name = custom_name

        if self.extension == ".mp4":
            self.video_to_audio()
            self.audio_to_text()
            self.text_to_summary()
        elif self.extension in [".mp3", ".wav"]:
            self.audio_file_path = self.media_path  # Directly use the given audio file
            self.audio_to_text()
            self.text_to_summary()
        elif self.extension == ".txt":
            self.transcript_path = (
                self.media_path
            )  # Directly use the given text file as transcript
            self.text_to_summary()
        else:
            raise UnsupportedFormatError(
                f"Unsupported file format: {self.extension}. Supported formats: .mp4, .mp3, .wav, .txt"
            )

        self.summary_to_notes()

    def video_to_audio(self):
        extract_audio(self.media_path)
        self.audio_file_path = f"./audio_files/{self.filename}.mp3"

    def audio_to_text(self, selected_model="small"):
        transcribe(audio_path=self.audio_file_path, model=selected_model)
        self.transcript_path = f"./transcripts/{self.filename}.txt"

    def text_to_summary(
        self, max_output_length: int = 1000, model: str = "gpt-3.5-turbo-0125"
    ):
        summarizer = OpenAISummarizer(self.transcript_path, model=model)
        summarizer.summarize(max_output_length)
        self.summary_path = f"./summaries/{self.filename}.json"

    def summary_to_notes(self):
        if self.output_format == "Markdown":
            try:
                page_builder = MarkdownPageBuilder(self.summary_path, self.custom_name)
                page_builder.create_page()
            except Exception as e:
                raise MarkdownPageError(
                    f"Could not create Markdown page. Error: {e}"
                ) from e
        elif self.output_format == "Notion":
            try:
                page_builder = NotionPageBuilder(self.summary_path, self.custom_name)
                page_builder.create_page()
            except Exception as e:
                raise NotionPageError(
                    f"Could not create Notion page. Error: {e}"
                ) from e


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
