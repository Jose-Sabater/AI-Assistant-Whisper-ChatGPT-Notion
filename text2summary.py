from openai import OpenAI
from config import settings
import os
import logging
import time
from utils.errors import SummarizationError, SaveError

client = OpenAI(
    api_key=settings.openai_api_key, organization=settings.openai_organization
)
logger = logging.getLogger(__name__)


class OpenAISummarizer:
    def __init__(
        self,
        transcript_path: str,
        max_input_tokens: int = 10000,
        model: str = "gpt-3.5-turbo-0125",
    ):
        """Initializes the Summarizer object.

        Args:
            transcript_path (str): Path to the transcript file
            max_input (int): Maximum number of tokens accepted per input, model-dependent
            model (str): Model to use for summarization
        """
        self.model = model
        self.max_input_tokens = max_input_tokens
        self.filename, _ = os.path.splitext(os.path.basename(transcript_path))
        with open(transcript_path, "r", encoding="utf-8") as f:
            self.transcript = f.read()

        if len(self.transcript.split(" ")) > max_input_tokens:
            logging.info("Transcript too large, splitting into chunks")
            self.chunks = self._split_chunks(self.transcript)
        else:
            self.chunks = [self.transcript]

    def _split_chunks(self, transcript: str):
        """Splits a transcript into chunks of max_tokens."""
        words = transcript.split(" ")
        chunks = []
        current_chunk = []
        current_tokens = 0
        for word in words:
            if current_tokens + len(word.split(" ")) > self.max_input_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_tokens = 0
            current_chunk.append(word)
            current_tokens += len(word.split(" "))
        if current_chunk:  # Add the last chunk if it's not empty
            chunks.append(" ".join(current_chunk))
        return chunks

    def summarize(
        self, max_output_length: int = 1000, save_summary: bool = True
    ) -> None:
        """Summarizes a transcript using the OpenAI API."""
        logging.info(f"Summarizing: {self.filename} with model: {self.model}.")

        responses = []
        for chunk in self.chunks:
            prompt = f"""Analyze the transcript provided below, then provide the following:
            Key "title:" - add a title.
            Key "summary" - create a summary.
            Key "main_points" - add an array of the main points. Limit each item to 80 words, and limit the list to 10 items.
            Key "action_items:" - add an array of action items. Limit each item to 50 words, and limit the list to 5 items.
            Key "follow_up:" - add an array of follow-up questions. Limit each item to 80 words, and limit the list to 5 items.
            Key "arguments:" - add an array of potential arguments against the transcript. Limit each item to 50 words, and limit the list to 5 items.
            Key "related_topics:" - add an array of topics related to the transcript. Limit each item to 50 words, and limit the list to 5 items.
            Key "sentiment" - add a sentiment analysis

            Ensure that the final element of any array within the JSON object is not followed by a comma.

            Transcript:

            {chunk}"""

            messages = [
                {
                    "role": "system",
                    "content": """You are an assistant that only speaks JSON. Do not write normal text.

            Example formatting:

            {
                "title": "Notion Buttons",
                "summary": "A collection of buttons for Notion",
                "action_items": [
                    "item 1",
                    "item 2",
                    "item 3"
                ],
                "follow_up": [
                    "item 1",
                    "item 2",
                    "item 3"
                ],
                "arguments": [
                    "item 1",
                    "item 2",
                    "item 3"
                ],
                "related_topics": [
                    "item 1",
                    "item 2",
                    "item 3"
                ]
                "sentiment": "positive"
            }
            """,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ]

            # communicate with the API
            logging.info("Sending prompt to OpenAI API...")
            for attempt in range(3):
                try:
                    response = client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        response_format={"type": "json_object"},
                        max_tokens=max_output_length,
                        temperature=0.1,
                        seed=42,
                    )
                    break
                except Exception as e:
                    if attempt == 2:
                        raise SummarizationError(
                            f"Could not send prompt to OpenAI API. Error: {e}"
                        ) from e
                    else:
                        logging.warning(
                            f"Could not send prompt to OpenAI API. Error: {e}. Retrying..."
                        )
                        time.sleep(5)

            logging.info("Received response from OpenAI API.")

            try:
                ai_output = response.choices[0].message.content
                logging.info(f"Total token use: {response.usage}")
            except Exception as e:
                raise SummarizationError(f"Could not parse response. Error: {e}") from e
            logging.info("Parsed response from OpenAI API.")

            responses.append(ai_output)
            logging.info("Appended response to responses list.")

        # save it to a file
        # ensure ./summaries directory exists
        if not os.path.exists("./summaries"):
            os.makedirs("./summaries")
        if save_summary == True:
            summary_path = f"./summaries/{self.filename}.json"
            try:
                with open(summary_path, "w") as f:
                    for response in responses:
                        f.write(response + "\n")
                    logging.info(f"Saved summary to {summary_path}.")
            except Exception as e:
                raise SaveError(f"Could not save summary to file. Error: {e}") from e
