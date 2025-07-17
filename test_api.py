import requests

file_path = r"C:\Users\lk502\OneDrive\Desktop\WhatsApp Ptt 2025-07-10 at 11.40.00 AM.ogg"
url = "http://localhost:8000/translate/"

with open(file_path, "rb") as audio_file:
    files = {"file": (file_path, audio_file, "audio/mp4")}
    data = {"target_lang": "hi"}

    response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        with open("translated_output.mp3", "wb") as f:
            f.write(response.content)
        print("✅ Translated audio saved as 'translated_output.mp3'")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
