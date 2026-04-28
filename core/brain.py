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

            if len(parts) < 3:
                return "format: evolve <file> <instruction>"

            return self.revolver.evolve(parts[1], parts[2])

        return None


    # =========================
    # PLUGIN / COMMAND THINK ENGINE
    # =========================
    def think(self, text):
        text = text.strip().lower()

        # log input
        self.remember(text, "input_received", intent="input")

        # -------------------------
        # AGENT MODE
        # -------------------------
        res = self.handle_agent(text)
        if res:
            self.remember(text, str(res), intent="agent", success=True)
            return res

        # -------------------------
        # EVOLVE MODE
        # -------------------------
        res = self.handle_evolve(text)
        if res:
            self.remember(text, str(res), intent="evolve", success=True)
            return res

        # -------------------------
        # COMMAND AI GENERATION
        # -------------------------
        cmds = self.cmd_ai.generate(text)

        last_error = ""

        for c in cmds:
            c = safe_command(c)

            if not c:
                continue

            try:
                result = engine.run(c)

                if result.get("success"):
                    output = f"⚙️ {c}\n{result['output']}"
                    self.remember(text, output, intent="execute", success=True)
                    return output

                last_error = result.get("output")

            except Exception as e:
                last_error = str(e)

        # fallback
        fallback = f"❌ gagal\n{last_error if last_error else 'no output'}"

        self.remember(text, fallback, intent="error", success=False)
        return fallback


# =========================
# RUNNER
# =========================
if __name__ == "__main__":
    brain = Brain()

    print("\n💬 Nano AI ACTIVE\n")

    while True:
        try:
            user = input("you> ")

            if user in ["exit", "quit"]:
                print("bye")
                break

            print("\n🧠 AI:\n", brain.think(user), "\n")

        except KeyboardInterrupt:
            print("\nbye")
            break

        except Exception as e:
            print("⚠️ error:", e)