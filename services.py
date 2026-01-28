import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=audio_file,
            response_format="json"
        )
    return transcription.text


def summarize_text(text):
    system_prompt = "You are a helpful assistant. Summarize the following podcast transcript into bullet points."
    messages_payload = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages_payload,
        temperature=0.5,
        max_tokens=1024
    )
    return completion.choices[0].message.content