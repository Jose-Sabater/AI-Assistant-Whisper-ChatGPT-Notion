# AI-Assistant
## Description
This application automates the tasks of taking notes from meetings. It can even be used to summarize any type of video
It takes a video file and finishes with a summary in your notion.
![AI Assistant](./assets/AI%20assistant.jpeg)

### 1. Video to Audio
Using the MoviePy library we take our ".mp4" file and extract its audio

### 2. Audio to text
In the transcription step with use Whisper, OpenAI's open source text transcription models. It takes the path to an audio file and returns its transcription

### 3. Text to Summary
Here we use Large Language Models, to summarize our text. Generating a summary, main bullet points , follow up points and other discussion topics. In the end also a sentiment analysis.  
Done using the OpenAI API and its latest model (has a cost per token)

### 4. Summary to Notion
Many people use notion as their note taking application, and this app is just a showcase of how to utilize their API. This step is rather simple and probably could be done with any other markdown language application that offers an API endpoint.

## Configuration
The app uses environment variables that contain our API keys and the notion path to our pages. You will need to create this .env or any other method to protect your files. Also you will need to modify the config.py

## Stack
python 
whisper(local not API)  
openai-api  
notion-api  
flask  
moviepy  

## Creator
José Sabater

## Acknowledgements
Inspiration from: https://www.youtube.com/watch?v=hCEdm9LGBb0&list=LL&index=13&t=20s

