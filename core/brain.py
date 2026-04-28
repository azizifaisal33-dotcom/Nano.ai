
# core/brain.py - FIXED VERSION (ganti bagian __init__ saja)

from core.revolver import Revolver  # ✅ ADD THIS IMPORT

class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.agent = Agent(self)  # ✅ Agent sekarang OK
        self.fs = FileSystem()
        self.backup = Backup()
        self.revolver = Revolver(self.fs, self.backup)  # ✅ FIXED: Tambah ini
        self.generator = NanoGenerator()
        self.session_id = str(uuid.uuid4())[:8]
        print(f"🧠 Nano BRAIN v2.5 | Session: {self.session_id}")