from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
import sys
import os

# Add project path for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

# ✅ Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Local imports (your modules)
from models.whisper_transcriber import WhisperModel
from models.translator_model import TranslationModel
from utils.audio_utils import save_uploaded_file, cleanup_temp_file
from utils.tts_utils import generate_speech

# Load models once
whisper_model = WhisperModel()
translator_model = TranslationModel()


# ✅ Text to Speech
@app.post("/text-to-speech/")
async def text_to_speech(
    background_tasks: BackgroundTasks,
    text: str = Form(...),
    target_lang: str = Form(...)
):
    if not text or not target_lang:
        raise HTTPException(status_code=400, detail="Text and language are required.")
    
    output_audio = "text_speech_output.mp3"
    generate_speech(text, lang=target_lang, output_path=output_audio)

    # ✅ Cleanup file after response is sent
    background_tasks.add_task(os.remove, output_audio)

    return FileResponse(
        output_audio,
        media_type="audio/mpeg",
        filename="text_speech_output.mp3"
    )


# ✅ Audio to Text with Language
@app.post("/audio-to-text/")
async def audio_to_text(
    file: UploadFile = File(...),
    target_lang: str = Form(...)
):
    if not file or not target_lang:
        raise HTTPException(status_code=400, detail="File and target language required")

    # Save temp file
    temp_audio = f"temp_{file.filename}"
    audio_data = await file.read()
    save_uploaded_file(audio_data, temp_audio)

    # Transcribe
    original_text = whisper_model.transcribe(temp_audio)

    # Translate if needed
    if target_lang != "en":
        translated_text = translator_model.translate(original_text, target_lang)
    else:
        translated_text = original_text

    # Clean up
    cleanup_temp_file(temp_audio)

    # Return both versions
    return {
        "original_text": original_text,
        "translated_text": translated_text,
        "target_lang": target_lang
    }



# ✅ Audio to Audio (Translate)
@app.post("/Audio to Audio/")
async def translate_audio(
    file: UploadFile = File(...),
    target_lang: str = Form(...)
):
    if not target_lang:
        raise HTTPException(status_code=400, detail="Target language is required.")

    print("✅ Requested language:", target_lang)

    # Save audio
    temp_audio = f"temp_{file.filename}"
    audio_data = await file.read()
    save_uploaded_file(audio_data, temp_audio)

    # Transcribe
    text = whisper_model.transcribe(temp_audio)
    print("📝 Transcribed:", text)

    # Translate
    translated_text = translator_model.translate(text, target_lang)
    print("🌍 Translated:", translated_text)

    # TTS
    output_audio = "translated_output.mp3"
    generate_speech(translated_text, lang=target_lang, output_path=output_audio)

    # Cleanup
    cleanup_temp_file(temp_audio)

    return FileResponse(output_audio, media_type="audio/mpeg", filename="translated_output.mp3")
#python -m uvicorn app:app --reload --port 8000
