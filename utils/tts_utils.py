from gtts import gTTS

def generate_speech(text, lang="hi", output_path="output.mp3"):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)
    return output_path
