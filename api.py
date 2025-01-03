from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from elevenlabs.client import ElevenLabs
import os
from pydub import AudioSegment

app = FastAPI()

# Initialize ElevenLabs client
API_KEY = "your_api_key_here"
AGENT_ID = "your_agent_id_here"
client = ElevenLabs(api_key=API_KEY)

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Save the uploaded audio file
        file_path = f"uploaded_audio/{file.filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Placeholder: Transcribe audio to text (requires a transcription service)
        user_input_text = "What is my insurance status?"  # Replace this with real transcription logic

        # Generate a response using ElevenLabs Conversational AI
        conversation = client.conversational_ai.Conversation(
            agent_id=AGENT_ID,
            user_input=user_input_text
        )
        response_text = conversation.generate_response()

        # Convert the response text to audio using ElevenLabs Text-to-Speech
        response_audio = client.text_to_speech(response_text)
        response_audio_path = "response_audio.wav"
        with open(response_audio_path, "wb") as f:
            f.write(response_audio)

        # Return the generated audio file
        return FileResponse(response_audio_path, media_type="audio/wav", filename="response.wav")
    except Exception as e:
        return {"error": str(e)}
