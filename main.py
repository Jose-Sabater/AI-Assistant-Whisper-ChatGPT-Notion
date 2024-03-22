import argparse
import logging
from assistant import NotesAssistant


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(
        description="Create notes from a video or audio file"
    )
    parser.add_argument("media_path", type=str, help="Path to the video or audio file")
    parser.add_argument(
        "--output_format",
        type=str,
        default="Markdown",
        help="Output format for notes (Notion or Markdown)",
    )
    parser.add_argument(
        "--custom_name", type=str, help="Custom name for the notes page"
    )
    args = parser.parse_args()

    assistant = NotesAssistant(args.media_path, args.output_format)
    assistant.make_notes(args.custom_name)


if __name__ == "__main__":
    main()

# example use
# python main.py /path/to/video.mp4 --output_format Notion --custom_name "My Notes"
