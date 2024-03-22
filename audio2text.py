import whisper
import numpy as np
from config import settings
import os
import torch
import logging
from utils.errors import TranscriptionError
from pyannote.audio import Pipeline
from utils.diarization import words_per_segment

logger = logging.getLogger(__name__)

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1", use_auth_token=settings.hf_token
)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pipeline.to(DEVICE)


def transcribe(
    audio_path: str,
    model: str = "small",
    include_diarization: bool = True,
) -> None:
    logging.info(f"Initializing Transcription with device: {DEVICE}")
    # Ensure ./transcripts directory exists
    if not os.path.exists("./transcripts"):
        os.makedirs("./transcripts")
    filename, _ = os.path.splitext(os.path.basename(audio_path))

    # Load the model
    try:
        model = whisper.load_model(
            model, device="cuda" if torch.cuda.is_available() else "cpu"
        )

        logging.info(
            f"""Model loaded, is multiligual {model.is_multilingual} and has
        {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."""
        )
    except Exception as e:
        logging.error(f"An error occurred while loading the model: {str(e)}")
        raise TranscriptionError(str(e))

    # Transcribe the audio
    try:
        transcription_result = model.transcribe(audio_path, word_timestamps=True)
        logging.info("Transcription completed successfully")
    except Exception as e:
        logging.error(f"An error occurred while transcribing the audio: {str(e)}")
        raise TranscriptionError(str(e))

    # Save the transcript
    with open(f"./transcripts/{filename}.txt", "w") as file:
        file.write(transcription_result["text"])
        logging.info(f"Transcript saved to ./transcripts/{filename}.txt")

    # Diarize the audio
    if include_diarization:
        try:
            diarization_result = pipeline(audio_path)
        except Exception as e:
            logging.error(f"An error occurred while diarizing the audio: {str(e)}")
            raise TranscriptionError(str(e))

        # Get the words per speaker
        final_result = words_per_segment(
            transcription_result,
            diarization_result,
            add_buffer=True,
            gap_scale_factor=0.5,
        )
        with open(f"./transcripts/{filename}_diarization.txt", "w") as file:
            for _, segment in final_result.items():
                file.write(
                    f'{segment["start"]:.3f}\t{segment["end"]:.3f}\t{segment["speaker"]}\t{segment["text"]}\n'
                )
            logging.info(
                f"diarization saved to ./transcripts/{filename}_diarization.txt"
            )
    logging.info("Transcription completed successfully")
