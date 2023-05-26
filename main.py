"""
Create a Class that takes in a video file and creates a Notion page out of it
Steps:
1. Convert video to audio
2. Transcribe audio to text
3. Summarize text
4. Create Notion page

You dont need to go through all the steps, you can just call the function that you want to use
"""
import logging
from datetime import datetime
from video_to_audio import convert_video_to_audio
from transcribe import transcribe_audio
from text_to_summary import summarize
from summary_to_notion import NotionPageBuilder
import os


class NotionPageError(Exception):
    """Raised when Notion page cannot be created"""

    pass


logging.basicConfig(level=logging.INFO)


class NotesAssistant:
    """Creates a Notion page out of a video file, using the following steps:

        1. Convert video to audio (using MoviePy library)
        2. Transcribe audio to text (using whisper library)
        3. Summarize text (using OpenAI API)
        4. Create Notion page (using Notion API)
    Usage: NotesAssistant(video_path="./videos/test_video.mp4")

    Methods:
        video_to_audio: Converts a video file to an audio file
        audio_to_text: Creates a transcript out of an audio file
        text_to_summary: Creates a summary out of a transcript
        summary_to_notion: Creates a Notion page out of a summary

    Notes:
    You dont need to go through all the steps, you can just call the function that you want to use

    Attributes:
        video_path: Path to the video file
        audio_file_path: Path to the audio file
        transcript_path: Path to the transcript file
        summary_path: Path to the summary file
    """

    def __init__(self, video_path: bool = None):
        self.video_path = video_path

    def video_to_audio(
        self,
        video_file: bool = None,
        save_audio: bool = True,
        save_path: str = "./audio_files",
        output_ext: str = "mp3",
    ):
        """Converts a video file to an audio file using MoviePy library"""
        if video_file is None:
            video_file = self.video_path
        audio_file_path, audio = convert_video_to_audio(
            self.video_path,
            save_audio=save_audio,
            save_path=save_path,
            output_ext=output_ext,
        )
        self.audio_file_path = audio_file_path
        return audio_file_path

    def audio_to_text(
        self,
        audio_file=None,
        selected_model="small.en",
        save_transcript: bool = True,
    ):
        """Creates a transcript out of an audio file using whisper library"""
        if audio_file is None:
            audio_file = self.audio_file_path

        transcript_path, raw_text = transcribe_audio(
            audio_file, save_transcript, selected_model
        )
        self.transcript_path = transcript_path
        return transcript_path

    def text_to_summary(
        self,
        transcript: None,
        model: str = "gpt-3.5-turbo-0301",
        save_summary: bool = True,
    ):
        """Creates a summary out of a transcript using OpenAI ChatGPT API"""
        if transcript is None:
            transcript = self.transcript_path
        summary_path = summarize(transcript, model=model, save_summary=save_summary)
        self.summary_path = summary_path
        return summary_path

    def summary_to_notion(self, summary: None):
        """Creates a Notion page out of a summary using Notion API"""
        if summary is None:
            summary = self.summary_path
        try:
            page = NotionPageBuilder(summary)
        except Exception as e:
            raise NotionPageError(f"Could not create Notion page. Error: {e}") from e

        try:
            page.create_page()
        except Exception as e:
            raise NotionPageError(f"Could not create Notion page. Error: {e}") from e
        logging.info("Notion page created successfully")


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
