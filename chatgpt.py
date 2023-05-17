import openai
from config import settings
import pandas as pd
import tiktoken

openai.organization = settings.openai_organization
openai.api_key = settings.openai_api_key

# pd.json_normalize(openai.Model.list(), "data").to_csv("models.csv")


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )


transcript_path = "./transcripts/data_utilization_short.txt"


def read_transcript(transcript_path):
    with open(transcript_path, "r", encoding="utf-8") as f:
        return f.read()


prompt = f"""Analyze the transcript provided below, then provide the following:
Key "title:" - add a title.
Key "summary" - create a summary.
Key "main_points" - add an array of the main points. Limit each item to 100 words, and limit the list to 10 items.
Key "action_items:" - add an array of action items. Limit each item to 100 words, and limit the list to 5 items.
Key "follow_up:" - add an array of follow-up questions. Limit each item to 100 words, and limit the list to 5 items.
Key "stories:" - add an array of an stories, examples, or cited works found in the transcript. Limit each item to 200 words, and limit the list to 5 items.
Key "arguments:" - add an array of potential arguments against the transcript. Limit each item to 100 words, and limit the list to 5 items.
Key "related_topics:" - add an array of topics related to the transcript. Limit each item to 100 words, and limit the list to 5 items.
Key "sentiment" - add a sentiment analysis

Ensure that the final element of any array within the JSON object is not followed by a comma.

Transcript:
        
        {read_transcript(transcript_path)}"""


messages = [
    {
        "role": "user",
        "content": prompt,
    },
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
]

model = "gpt-3.5-turbo-0301"
print(f"{num_tokens_from_messages(messages, model)} prompt tokens counted.")


response = openai.ChatCompletion.create(
    model=model, messages=messages, max_tokens=1000, temperature=0.2
)
ai_output = response["choices"][0]["message"]["content"]


# save it to a file
with open("./summaries/data_utilization_out.json", "w") as f:
    f.write(ai_output)
