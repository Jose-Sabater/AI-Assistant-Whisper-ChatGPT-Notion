""" Custom error messages for the application """


class SummarizationError(Exception):
    """Raised when a transcript cannot be summarized."""

    pass


class SaveError(Exception):
    """Raised when a file cannot be saved."""

    pass


class ConversionError(Exception):
    """Custom exception for errors during conversion process."""

    pass


class TranscriptionError(Exception):
    """Custom exception for errors during transcription process."""

    pass


class UnsupportedFormatError(Exception):
    """Custom exception for unsupported file formats."""

    pass


class NotionPageError(Exception):
    """Raised when Notion page cannot be created"""

    pass


class MarkdownPageError(Exception):
    """Raised when Notion page cannot be created"""

    pass
