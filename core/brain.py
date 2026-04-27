import os

from core.command_ai import CommandAI
from core.agent import Agent
from core.revolver import Revolver

# asumsi kamu sudah punya engine & fs & backup
from core.engine import engine


class FileSystem:
    def read(self, path):
        with open(path, "r") as f:
            return f.read()

    def write(self, path, content):
        with open(path, "w") as f:
            f.write(content)


class DummyBackup:
    def create(self):
        # minimal backup (biar tidak error kalau belum ada sistem backup)
        try:
            os.system("cp core/brain.py core/brain.py.bak")
        except:
            pass


class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.agent = Agent(self)

        self.fs = FileSystem()
        self.backup = DummyBackup()
        self.revolver = Revolver(self.fs, self.backup)

    # =========================
    # CORE THINK
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

                if result["success"] and result["output"]:
                    return f"⚙️ {c}\n{result['output']}"

                else:
                    last_error = result.get("output", "")

            except Exception as e:
                last_error = str(e)

        # =====================
        # FAIL
        # =====================
        return f"❌ gagal\n{last_error}"