import os
import logging
from moviepy.editor import VideoFileClip
from utils.errors import ConversionError
from typing import Optional


logger = logging.getLogger(__name__)

# TODO Revise the filename if we want to read from file name or pass it through the classes


def extract_audio(
    video_path: str,
    output_ext: Optional[str] = "mp3",
    save_path: Optional[str] = "./audio_files",
):
    """Converts video to audio using MoviePy"""
    if not os.path.isfile(video_path):
        logging.error(f"The file {video_path} does not exist.")
        raise ConversionError(f"The file {video_path} does not exist.")

    file_path, ext = os.path.splitext(video_path)
    # get the name of the video file
    filename = file_path.split("/")[-1]
    output_dir = save_path
    output_file = f"{output_dir}/{filename}.{output_ext}"

    # Check if output directory exists, create if not
    if not os.path.isdir(output_dir):
        logging.info(f"Directory {output_dir} not found. Creating it.")
        os.makedirs(output_dir)

    try:
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(output_file)
        logging.info(f"Audio extracted successfully, file saved to {output_file}")
        return output_file, clip.audio
    except Exception as e:
        logging.error(
            f"An error occurred while converting {video_path} to audio: {str(e)}"
        )
        raise ConversionError(str(e)) from e


if __name__ == "__main__":
    extract_audio("./videos/elon.mp4")
