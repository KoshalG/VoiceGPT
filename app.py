from flask import Flask, Response, request
from gtts import gTTS
import os
import openai
import warnings
import io

warnings.filterwarnings("ignore")
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    # transcribes the audio data from the request
    audio_data = request.data
    transcript = openai.Audio.transcribe("whisper-1", audio_data)
    return transcript

@app.route("/tts", methods=["POST"])
def tts():
    # converts text to speech using gTTS
    text = request.data.decode()
    audio_obj = gTTS(text=text, lang="en", slow=False)
    audio_data = io.BytesIO()
    audio_obj.write_to_fp(audio_data)
    audio_data.seek(0)

    headers = {
        'Content-Type': 'audio/mpeg',
        'Content-Disposition': 'attachment; filename="audio.mp3"'
    }
    return Response(audio_data, headers=headers)

@app.route("/chat", methods=["POST"])
def chat():
    # uses OpenAI GPT-3 to generate a response
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    input_text = request.data.decode()
    if input_text:
        messages.append({"role": "user", "content": input_text})
        chat_completion = openai.Completion.create(model="chatgpt-3.5-turbo", messages=messages)
        reply = chat_completion.choices[0].text
    else:
        reply = "I didn't get that. Can you try again?"
    return reply

if __name__ == '__main__':
    app.run()