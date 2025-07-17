import os

def save_uploaded_file(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file)
    return save_path

def cleanup_temp_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
