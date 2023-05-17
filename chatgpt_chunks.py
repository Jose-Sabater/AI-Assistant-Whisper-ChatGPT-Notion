import openai
from config import settings
import pandas as pd
import tiktoken
from tiktoken import Tokenizer

openai.organization = settings.openai_organization
openai.api_key = settings.openai_api_key

model = "gpt-3.5-turbo-0301"


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


transcript_path = "./transcripts/data_utilization.txt"


def read_transcript(transcript_path):
    with open(transcript_path, "r", encoding="utf-8") as f:
        return f.read()


def split_transcript(transcript, max_tokens):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(transcript)
    chunks = []
    current_chunk = ""
    current_tokens = 0
    for token in tokens:
        if current_tokens + len(token) > max_tokens:
            chunks.append(current_chunk)
            current_chunk = ""
            current_tokens = 0
        current_chunk += token
        current_tokens += len(token)
    if current_chunk:  # Add the last chunk if it's not empty
        chunks.append(current_chunk)
    return chunks


transcript = read_transcript(transcript_path)
chunks = split_transcript(
    transcript, 2000
)  # Adjust the token limit based on your messages

responses = []
for chunk in chunks:
    prompt = f"""Analyze the transcript provided below, then provide the following:
    #... your prompt here ...

    Transcript:

    {chunk}"""

    messages = [
        # ... your messages here ...
        {
            "role": "user",
            "content": prompt,
        },
        # ... your system message here ...
    ]

    response = openai.ChatCompletion.create(
        model=model, messages=messages, max_tokens=1000, temperature=0.2
    )
    ai_output = response["choices"][0]["message"]["content"]
    responses.append(ai_output)

# save it to a file
with open("./data_utilization.json", "w") as f:
    for response in responses:
        f.write(response + "\n")
