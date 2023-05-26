"""We will have several segments:
- Video to Audio
- Audio to Text using whisper
    - Count tokens
- Text to summary using ChatGPT API
- Summary to Notion using Notion API
"""
import logging
from datetime import datetime
from video_to_audio import convert_video_to_audio
from transcribe import transcribe_audio
from text_to_summary import summarize
import os


class NotesAssistant:
    def __init__(self, video_path: bool = None):
        """Initializes the NotesAssistant class"""
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

    def summary_to_notion(self):
        pass


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
