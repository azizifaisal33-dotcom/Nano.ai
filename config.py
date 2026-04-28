"""
⚙️ NanoAI Config - 100% Custom
Hanya berisi pengaturan sistem dasar.
"""

class Config:
    def __init__(self):
        self.NAME = "NanoAI"
        self.VERSION = "2.0-STABLE"
        self.BASE_DIR = "data"
        self.LOG_FILE = "logs/session.log"
        
        # Pengaturan untuk Generator buatanmu sendiri
        self.MAX_GEN_LENGTH = 12
        self.EVOLVE_THRESHOLD = 0.5

    def get_system_prompt(self):
        return f"Kamu adalah {self.NAME}, asisten terminal yang belajar dari nol."

config = Config()
