# AI-Assistant
## Description
The AI-Assistant is a versatile tool designed to streamline the process of note-taking from various media formats such as videos, audios, and meetings. It simplifies the creation of concise summaries, making it invaluable for capturing key points and insights. Whether starting from a video file, an audio clip, or a transcript, the application supports both GPU and CPU environments for efficient processing.  
![AI Assistant](./assets/AI%20assistant.jpeg)

## Workflow

### 1. Video to Audio
- Tool: MoviePy library.
- Function: Converts ".mp4" files into audio for further processing.

---
### 2. Audio to text
- Tool: Whisper, OpenAI's open-source transcription model, and pyannote for diarization.
- Function: Transcribes audio files, offering support for multiple languages and speaker identification.
- Models: Default to the small model, with options to switch as per the user's requirement. [Available Models](https://github.com/openai/whisper)

Diarization(speaker identification) is available. This is built using pyannote, and some custom utils from https://github.com/Jose-Sabater/whisper-pyannote

---
### 3. Text to Summary
- Tool: Large Language Models.
- Function: Generates comprehensive summaries including main points, follow-up queries, discussion topics, and sentiment analysis using the [JSON mode](https://platform.openai.com/docs/guides/text-generation/json-mode).
- Expansion: Future updates will include support for additional models.

---
### 4. Summary to Notes
- Function: Converts summaries into organized blocks, capturing summaries, action items, follow-ups, arguments, related topics, sentiments, and dates.
- Formats: Supports output in Notion for seamless integration into workflows or Markdown for local documentation.  

**Notion Integration**
Illustrates how to leverage the Notion API for note integration, showcasing the potential for adaptation to other Markdown-supported platforms.  

**Markdown Output**
Generates a local Markdown document encompassing all insights derived from the analysis.


## Configuration
To protect your API keys and Notion paths, it's recommended to utilize environment variables, stored in a .env file or a similar secure method. The application's configuration settings are automatically loaded from the config.py file, ensuring all necessary credentials are in place.

## Usage
To begin, ensure all dependencies are installed:
```shell
pip install -r requirements.txt
```
The application can process mp4 files, audio, or text transcripts. Here are some ways to use AI-Assistant:
#### *Python*  
```python
import logging
from assistant import NotesAssistant

logging.basicConfig(level=logging.INFO)

# Specify your media file and desired output format
assistant = NotesAssistant("./transcripts/neuralink.txt", "Markdown")
# Execute the note-making process
assistant.make_notes("fireship-neuralink")
```

#### *CLI*
```bash
python main.py /path/to/media --output_format Notion --custom_name "My Notes"
```

#### *Flask*
If you want to experiment a minimalistic flask app is available.
From your terminal / Shell
```
python flask_app.py
```

## Example
View a generated [Notion Page](https://great-xenon-74b.notion.site/fireship-neuralink-693da8c633b34bb9b971eef50168237c?pvs=4)


## Logs:
Sample application logs to illustrate the process flow:
```
MoviePy - Writing audio in ./audio_files/neuralink.mp3
INFO:root:Audio extracted successfully, file saved to ./audio_files/neuralink.mp3
INFO:root:Initializing Transcription with device: cuda
MoviePy - Done.
INFO:root:Model loaded, is multiligual True and has
        240,582,912 parameters.
INFO:root:Transcription completed successfully
INFO:root:Transcript saved to ./transcripts/neuralink.txt
INFO:root:diarization saved to ./transcripts/neuralink_diarization.txt
INFO:root:Transcription completed successfully
INFO:root:Summarizing: neuralink with model: gpt-3.5-turbo-0125.
INFO:root:Sending prompt to OpenAI API...
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:root:Received response from OpenAI API.
INFO:root:Total token use: CompletionUsage(completion_tokens=563, prompt_tokens=1549, total_tokens=2112)
INFO:root:Parsed response from OpenAI API.
INFO:root:Appended response to responses list.
INFO:root:Saved summary to ./summaries/neuralink.json.
INFO:root:PageBuilder initialized.
INFO:root:Creating Notion page.
INFO:httpx:HTTP Request: POST https://api.notion.com/v1/pages "HTTP/1.1 200 OK"
INFO:root:Page created successfully.
```

## Stack
python  
whisper  
pyannote  
openai - gpt  
notion-api    
moviepy  
flask  

## References
https://github.com/pyannote/pyannote-audio  
https://pypi.org/project/openai-whisper/  
https://developers.notion.com/
https://huggingface.co/openai/whisper-large-v3  



## Author
José Sabater

## License
MIT

