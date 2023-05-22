"""We will have several segments:
- Video to Audio
- Audio to Text using whisper
    - Count tokens
- Text to summary using ChatGPT API
- Summary to Notion using Notion API
"""

from video_to_audio import convert_video_to_audio
from transcribe import transcribe_audio
import logging
from datetime import datetime


class NotesAssistant:
    def __init__(self, video_path: str):
        self.video_path = video_path

    def video_to_audio(
        self,
        audio_file: str,
        save_audio: bool = True,
        save_path: str = "./audio_files",
        output_ext: str = "mp3",
    ):
        """Converts a video file to an audio file using MoviePy library"""

        audio_file, audio = convert_video_to_audio(self.video_path)
        self.audio_file = audio_file
        return audio_file

    def audio_to_text(
        self,
        audio_file=None,
        selected_model="small.en",
        save_transcript: bool = True,
        transcript_path: str = "./transcripts",
    ):
        """Creates a transcript out of an audio file using whisper library"""
        if audio_file is None:
            audio_file = self.audio_file

        transcript, raw_text = transcribe_audio(
            audio_file, selected_model, save_transcript=save_transcript
        )
        self.transcript = transcript
        return transcript

    def audio_to_summary(self):
        pass

    def summary_to_notion(self):
        pass


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
