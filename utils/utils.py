import tiktoken


def count_tokens_openai(messages: list[dict[str, str]], model: str) -> int:
    """Counts the number of tokens in a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    try:
        num_tokens = 0
        for message in messages:
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
        return num_tokens
    except Exception as e:
        raise Exception(f"Error counting tokens: {e}") from e


# print(count_tokens_openai([{"key": "This is great"}], "gpt-3.5-turbo-0125"))
