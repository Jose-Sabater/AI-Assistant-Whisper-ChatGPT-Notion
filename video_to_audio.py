import os
import sys
import logging
from moviepy.editor import VideoFileClip


logger = logging.getLogger(__name__)


class ConversionError(Exception):
    """Custom exception for errors during conversion process."""


def convert_video_to_audio(
    video_file: str,
    save_audio: bool = True,
    save_path: str = "./audio_files",
    output_ext: str = "mp3",
) -> tuple[str, VideoFileClip]:
    """Converts video to audio using MoviePy library"""
    if not os.path.isfile(video_file):
        logging.error(f"The file {video_file} does not exist.")
        raise ConversionError(f"The file {video_file} does not exist.")

    file_path, ext = os.path.splitext(video_file)
    # get the name of the video file
    filename = file_path.split("/")[-1]
    output_dir = save_path
    output_file = f"{output_dir}/{filename}.{output_ext}"

    # Check if output directory exists, create if not
    if not os.path.isdir(output_dir):
        logging.info(f"Directory {output_dir} not found. Creating it.")
        os.makedirs(output_dir)

    try:
        clip = VideoFileClip(video_file)
        if save_audio:
            clip.audio.write_audiofile(output_file)
        return output_file, clip.audio
    except Exception as e:
        logging.error(
            f"An error occurred while converting {video_file} to audio: {str(e)}"
        )
        raise ConversionError(str(e))



