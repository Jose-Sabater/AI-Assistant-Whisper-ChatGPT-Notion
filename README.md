# AI-Assistant
## Description
This application automates the tasks of taking notes from videos, audios, meetings. It can even be used to summarize any type of video
It takes a video file and finishes with a summary in your notion. You can also start on any of the other steps (audio or transcript).  
Runs on GPU or CPU
![AI Assistant](./assets/AI%20assistant.jpeg)

### 1. Video to Audio
Using the MoviePy library we take our ".mp4" file and extract its audio

---
### 2. Audio to text
In the transcription step with use Whisper, OpenAI's open source transcription models. It takes the path to an audio file and returns its transcription.  By default uses small model. See available models here: https://github.com/openai/whisper   

Diarization(speaker identification) is available. This is built using pyannote, and some custom utils from https://github.com/Jose-Sabater/whisper-pyannote

---
### 3. Text to Summary
Here we use Large Language Models, to summarize our text. Generating a summary, main bullet points , follow up points and other discussion topics. In the end also a sentiment analysis. This project uses the [JSON mode](https://platform.openai.com/docs/guides/text-generation/json-mode), verify that the models you select have it.  
For now this step is done using OpenAI, but will include availability to more models

---
### 4. Summary to Notes
We create blocks according to everything we want to extract from the transcript:  
Summary, action items, follow up, arguments, related topics, sentiment, date  

2 Options Notion or Markdown  
#### Notion
Many people use notion as their note taking application, and this app is just a showcase of how to utilize their API. This step is rather simple and probably could be done with any other markdown language application that offers an API endpoint. 
#### Markdown
Generates a local markdown page with the found insights.


## Configuration
The app uses environment variables that contain our API keys and the notion path to our pages. You will need to create this .env or any other method to protect your secrets.  
Everything is loaded automatically through the [config](./config.py) file, so be sure to have all the required keys.

## Usage
```shell
pip install -r requirements.txt
```
To get started you can have a mp4, an audio file or a transcript
#### *Python*  
```python
import logging
from assistant import NotesAssistant

logging.basicConfig(level=logging.INFO)

assistant = NotesAssistant("./transcripts/neuralink.txt", "Markdown") # Point it to your media
assistant.make_notes("fireship-neuralink") # Performs all needed steps until notes are ready
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

