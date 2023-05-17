import os
import sys
from moviepy.editor import VideoFileClip


def convert_video_to_audio_moviepy(video_file, output_ext="mp3"):
    """Converts video to audio using MoviePy library
    that uses `ffmpeg` under the hood"""
    file_path, ext = os.path.splitext(video_file)
    # get the name of the video file
    filename = file_path.split("/")[-1]
    clip = VideoFileClip(video_file)
    clip.audio.write_audiofile(f"./audio_files/{filename}.{output_ext}")


if __name__ == "__main__":
    vf = sys.argv[1]
    convert_video_to_audio_moviepy(vf)

    #usage in cmd: python video_to_audio.py ./videos/test_video.mp4