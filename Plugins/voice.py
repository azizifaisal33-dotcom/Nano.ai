# Whisper STT (lightweight)
def speech_to_text():
    subprocess.run("pkg install ffmpeg", shell=True)
    # termux-microphone-record → Whisper