from flask import Flask, Response, request
from gtts import gTTS
import os
import openai
import warnings
import io

warnings.filterwarnings("ignore") # ignore warnings
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/transcribe", methods=["POST"]) # POST request to /transcribe
def transcribe():
    # transcribes the audio data from the request
    audio_data = request.files.get("file")
    transcript = openai.Audio.transcribe("whisper-1", audio_data.read())
    
    # generate response from OpenAI GPT-3 using transcribed text as prompt
    messages = [{"role": "user", "content": transcript}]
    chat_completion = openai.Completion.create(model="chatgpt-3.5-turbo", messages=messages)
    reply = chat_completion.choices[0].text

    # convert text response to audio
    audio_obj = gTTS(text=reply, lang="en", slow=False)
    audio_data = io.BytesIO()
    audio_obj.write_to_fp(audio_data)
    audio_data.seek(0)

    headers = {
        'Content-Type': 'audio/mpeg',
        'Content-Disposition': 'attachment; filename="audio.mp3"'
    }
    return Response(audio_data, headers=headers)

if __name__ == '__main__':
    app.run()