from main import NotesAssistant
import logging

logging.basicConfig(level=logging.INFO)

assistant = NotesAssistant(video_path="./videos/test_video.mp4")
audio_file = assistant.video_to_audio()
transcript = assistant.audio_to_text(audio_file)
summary = assistant.text_to_summary(transcript)
