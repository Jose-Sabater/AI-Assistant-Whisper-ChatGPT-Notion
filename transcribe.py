import whisper
import numpy as np
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# audio_file = "./audio_files/test_video.mp3"
audio_file = "./audio_files/data_utilization.mp3"
filename = "data_utilization"

model_size = "small.en"

model = whisper.load_model(model_size)
print(
    f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
    f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."
)

# predict without timestamps for short-form transcription

audio = whisper.load_audio(audio_file)
print(audio.shape)

# audio = whisper.pad_or_trim(audio)
# print(audio.shape)
# # make log-Mel spectrogram and move to the same device as the model
# mel = whisper.log_mel_spectrogram(audio).to(model.device)

# # detect the spoken language
# _, probs = model.detect_language(mel)
# print(f"Detected language: {max(probs, key=probs.get)}")

# # transcribe the speech
# options = whisper.DecodingOptions(language="en")
# result = whisper.decode(model, mel, options=options)

result = model.transcribe(audio_file)

with open(f"./transcripts/{filename}.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

print(result["text"])
