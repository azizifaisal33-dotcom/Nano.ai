"""
⚙️ NanoEngine - Lightweight Execution Core
No Torch, No Transformers - 100% Termux Stable
"""
from config import config

class NanoEngine:
    def __init__(self):
        # Kita matikan load model Transformers agar tidak ModuleNotFoundError
        print("⚙️ Engine: Lightweight Mode Active (No Torch)")

    def run(self, command: str):
        """Menjalankan perintah sistem melalui shell Termux"""
        import subprocess
        try:
            # Jalankan command dan ambil outputnya
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            return {"output": result, "success": True}
        except subprocess.CalledProcessError as e:
            return {"output": e.output, "success": False}
        except Exception as e:
            return {"output": str(e), "success": False}

    def generate(self, user_input: str):
        """
        Fallback generator jika model Transformers tidak ada.
        Bisa diarahkan ke NanoGenerator di core/generator.py
        """
        return f"NanoAI: Eksekusi perintah '{user_input}' selesai."

# Global instance agar bisa dipanggil oleh nano.py atau brain.py
engine = NanoEngine()
