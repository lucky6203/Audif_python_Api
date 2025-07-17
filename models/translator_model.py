# models/translator_model.py
from deep_translator import GoogleTranslator

class TranslationModel:
    def __init__(self):
        pass  # No need to initialize a translator instance

    def translate(self, text: str, target_lang: str) -> str:
        try:
            return GoogleTranslator(source='auto', target=target_lang).translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return "Translation failed."