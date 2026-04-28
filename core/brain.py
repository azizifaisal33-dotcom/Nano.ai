import uuid
import os

from core.command_ai import CommandAI
from core.agent import Agent
from core.revolver import Revolver
from core.engine import engine
from core.memory import memory
from core.knowledge_builder import search_knowledge, add_knowledge


# =========================
# SAFE COMMAND FILTER
# =========================
def safe_command(cmd):
    blacklist = [
        "rm -rf",
        "shutdown",
        "reboot",
        "sudo",
        "mkfs",
        "dd if="
    ]

    return None if any(b in cmd for b in blacklist) else cmd


# =========================
# DEPENDENCY SYSTEM
# =========================
class FileSystem:
    def read(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def write(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


class Backup:
    def create(self):
        try:
            os.system("cp core/brain.py core/brain_backup.py")
        except:
            pass


# =========================
# BRAIN CORE SYSTEM
# =========================
class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.agent = Agent(self)

        # FIX: Revolver MUST have dependencies
        self.revolver = Revolver(FileSystem(), Backup())

        self.session_id = str(uuid.uuid4())[:10]

        print("🧠 Nano AI BRAIN ONLINE")

    # =========================
    # MEMORY WRAPPER
    # =========================
    def remember(self, user, ai, intent="chat"):
        memory.add(self.session_id, user, ai, intent=intent)

    # =========================
    # SIMPLE CHAT FALLBACK
    # =========================
    def chat(self, text):
        t = text.lower()

        if "halo" in t:
            return "Halo 👋 aku NanoAI"
        if "siapa kamu" in t:
            return "Aku NanoAI system kamu"
        if "nama" in t:
            return "Namaku NanoAI"

        return "Aku belum paham, tapi aku belajar 🤖"

    # =========================
    # THINK ENGINE (MAIN AI PIPELINE)
    # =========================
    def think(self, text):
        text = text.strip().lower()

        # =========================
        # [1] KNOWLEDGE LAYER (FASTEST)
        # =========================
        kb = search_knowledge(text)
        if kb:
            self.remember(text, kb, "knowledge")
            return kb

        # =========================
        # [2] MEMORY LAYER
        # =========================
        mem = memory.search(text)
        if mem:
            response = mem[0]["ai