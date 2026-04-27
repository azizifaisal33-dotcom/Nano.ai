import os
import subprocess

from core.command_ai import CommandAI
from core.agent import Agent
from core.revolver import Revolver
from core.engine import engine


# =========================
# FILE SYSTEM SAFE
# =========================
class FileSystem:
    def read(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def write(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


# =========================
# BACKUP SAFE
# =========================
class DummyBackup:
    def create(self):
        try:
            os.system("cp core/brain.py core/brain_backup.py")
        except:
            pass


# =========================
# SAFETY FILTER (IMPORTANT)
# =========================
def safe_command(cmd: str):
    blacklist = [
        "rm -rf",
        "shutdown",
        "reboot",
        "git pull",
        "git push",
        "nano",
        "vim",
        "sudo"
    ]

    for b in blacklist:
        if b in cmd:
            return None

    return cmd


# =========================
# MAIN BRAIN
# =========================
class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.agent = Agent(self)

        self.fs = FileSystem()
        self.backup = DummyBackup()
        self.revolver = Revolver(self.fs, self.backup)

        self.model_path = self.find_model()

        print("🧠 Nano AI Brain ONLINE")

        if not self.model_path:
            print("⚠️ model GGUF tidak ditemukan di folder models/")

    # =========================
    # AUTO DETECT GGUF
    # =========================
    def find_model(self):
        if os.path.isfile("./models/model.gguf"):
            return "./models/model.gguf"

        if os.path.isdir("./models"):
            for f in os.listdir("./models"):
                if f.endswith(".gguf"):
                    return os.path.join("./models", f)

        return None

    # =========================
    # AGENT MODE
    # =========================
    def handle_agent(self, text):
        if text.startswith("agent"):
            if "start" in text:
                goal = text.replace("agent start", "").strip()
                return self.agent.start(goal)

            if "stop" in text:
                return self.agent.stop()

            if "log" in text:
                return self.agent.log()

        return None

    # =========================