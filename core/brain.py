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
# MAIN BRAIN
# =========================
class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.agent = Agent(self)

        self.fs = FileSystem()
        self.backup = DummyBackup()
        self.revolver = Revolver(self.fs, self.backup)

        # =====================
        # GGUF / LLAMA CONFIG
        # =====================
        self.model_path = self.find_model()

        print("🧠 Nano AI Brain Ready")

        if not self.model_path:
            print("⚠️ model GGUF tidak ditemukan di folder models/")

    # =========================
    # AUTO DETECT GGUF
    # =========================
    def find_model(self):
        possible = [
            "./models/model.gguf",
            "./model.gguf",
            "./models/"
        ]

        for p in possible:
            if os.path.isfile(p):
                return p

        # kalau folder models ada, ambil file pertama gguf
        if os.path.isdir("./models"):
            for f in os.listdir("./models"):
                if f.endswith(".gguf"):
                    return os.path.join("./models", f)

        return None

    # =========================
    # THINK CORE
    # =========================
    def think(self, text):
        text = text.strip().lower()

        # =====================
        # AGENT MODE
        # =====================
        if text.startswith("agent"):
            if "start" in text:
                goal = text.replace("agent start", "").strip()
                return self.agent.start(goal)

            if "stop" in text:
                return self.agent.stop()

            if "log" in text:
                return self.agent.log()

        # =====================
        # EVOLVE MODE
        # =====================
        if text.startswith("evolve"):
            parts = text.split(" ", 2)

            if len(parts) < 3:
                return "format: evolve <file> <instruksi>"

            file = parts[1]
            instr = parts[2]

            return self.revolver.evolve(file, instr)

        # =====================
        # COMMAND MODE
        # =====================
        cmds = self.cmd_ai.generate(text)

        last_error = ""

        for c in cmds:
            try:
                result = engine.run(c)

                if result.get("success") and result.get("output"):
                    return f"⚙️ {c}\n{result['output']}"

                last_error = result.get("output", "")

            except Exception as e:
                last_error = str(e)

        # =====================
        # FAIL SAFE
        # =====================
        return f"❌ gagal\n{last_error if last_error else 'no output'}"