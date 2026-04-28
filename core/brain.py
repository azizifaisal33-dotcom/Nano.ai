import os
import sys
import uuid

# =========================
# PATH FIX
# =========================
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.command_ai import CommandAI
from core.agent import Agent
from core.revolver import Revolver
from core.engine import engine
from core.memory import memory


# =========================
# SAFE FILE SYSTEM
# =========================
class FileSystem:
    def read(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def write(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


# =========================
# BACKUP SYSTEM
# =========================
class Backup:
    def create(self):
        try:
            os.system("cp core/brain.py core/brain_backup.py")
        except:
            pass


# =========================
# SAFETY FILTER
# =========================
def safe_command(cmd):
    blacklist = [
        "rm -rf",
        "shutdown",
        "reboot",
        "git pull",
        "git push",
        "sudo",
        "mkfs",
        "dd if="
    ]

    for b in blacklist:
        if b in cmd:
            return None

    return cmd


# =========================
# MAIN BRAIN (CORE AI OS)
# =========================
class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.agent = Agent(self)
        self.revolver = Revolver(FileSystem(), Backup())

        self.session_id = str(uuid.uuid4())[:10]

        print("🧠 Nano AI BRAIN ONLINE")


    # =========================
    # MEMORY WRAPPER
    # =========================
    def remember(self, user_input, ai_output, intent="chat", success=True):
        memory.add(
            self.session_id,
            user_input,
            ai_output,
            intent=intent,
            tool_used="brain",
            success=success
        )


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
    # EVOLVE MODE (REVOLVER)
    # =========================
    def handle_evolve(self, text):
        if text.startswith("evolve"):
            parts = text.split(" ", 2)

            if