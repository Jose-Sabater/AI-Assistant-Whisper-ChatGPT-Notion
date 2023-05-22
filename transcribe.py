import whisper
import numpy as np
import torch
import os
import logging


logger = logging.getLogger(__name__)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class TranscriptionError(Exception):
    """Custom exception for errors during transcription process."""


def transcribe_audio(
    audio_file: str,
    save_transcript: bool = True,
    selected_model: str = "small.en",
    transcript_path: str = "./transcripts",
) -> tuple[str, str]:
    """Creates a transcript out of an audio file using whisper library

    Args:
        audio_file (str): path to audio file
        save_transcript (bool, optional): whether to save the transcript. Defaults to True.
        selected_model (str, optional): model to use for transcription. Defaults to "small.en".
        transcript_path (str, optional): path to save the transcript. Defaults to "./transcripts".

    Returns:
        tuple[str, str]: path to transcript file, raw text



    """
    logging.info(f"Using device: {DEVICE}")

    filename, _ = os.path.splitext(os.path.basename(audio_file))
    try:
        model = whisper.load_model(selected_model)

        logging.info(
            f"""Model is {model.is_multilingual} and has
        {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."""
        )

    except Exception as e:
        logging.error(f"An error occurred while loading the model: {str(e)}")
        raise TranscriptionError(str(e))

    try:
        audio = whisper.load_audio(audio_file)
        print(f"Audio is {audio.duration:.1f} seconds long.")

    except Exception as e:
        logging.error(f"An error occurred while loading the audio: {str(e)}")
        raise TranscriptionError(str(e))

    try:
        result = model.transcribe(audio_file)

    except Exception as e:
        logging.error(f"An error occurred while transcribing the audio: {str(e)}")
        raise TranscriptionError(str(e))

    # Check if output directory exists, create if not
    if not os.path.isdir(transcript_path):
        os.makedirs(transcript_path)

    transcript = f"{transcript_path}/{filename}.txt"

    if save_transcript:
        try:
            with open(transcript, "w", encoding="utf-8") as f:
                f.write(result["text"])
        except Exception as e:
            logging.error(f"An error occurred while saving the transcript: {str(e)}")
            raise TranscriptionError(str(e))

    return transcript, result["text"]
