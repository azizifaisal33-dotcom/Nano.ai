# espeak-ng TTS
def speak(text):
    subprocess.run(f"termux-tts-speak '{text}'", shell=True)