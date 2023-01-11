import whisper

model = whisper.load_model("large-v2")
print("Transcribing...")
result = model.transcribe(r"download.mp3")
print(result["text"])
