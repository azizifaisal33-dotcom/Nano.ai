import uuid

from core.command_ai import CommandAI
from core.agent import Agent
from core.revolver import Revolver
from core.engine import engine
from core.memory import memory


# =========================
# SAFE COMMAND
# =========================
def safe_command(cmd):
    blacklist = ["rm -rf", "shutdown", "reboot", "sudo", "mkfs", "dd if="]
    return None if any(b in cmd for b in blacklist) else cmd


# =========================
# BRAIN CORE
# =========================
class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.agent = Agent(self)
        self.revolver = Revolver()
        self.session_id = str(uuid.uuid4())[:10]

        print("🧠 Nano AI BRAIN ONLINE")

    # =========================
    # INTENT DETECTOR
    # =========================
    def detect_intent(self, text):
        t = text.lower()

        if t.startswith("agent"):
            return "agent"
        if t.startswith("evolve"):
            return "evolve"

        chat_words = ["halo", "hai", "siapa", "nama", "apa", "kenapa", "how", "what"]
        if any(w in t for w in chat_words):
            return "chat"

        return "command"

    # =========================
    # CHAT RESPONSE
    # =========================
    def chat(self, text):
        t = text.lower()

        if "halo" in t or "hai" in t:
            return "Halo 👋 aku NanoAI"
        if "siapa kamu" in t:
            return "Aku NanoAI system kamu"
        if "nama" in t:
            return "Namaku NanoAI"

        return "Aku belum paham, tapi aku belajar 🤖"

    # =========================
    # MEMORY WRAPPER
    # =========================
    def remember(self, user, ai, intent):
        memory.add(self.session_id, user, ai, intent=intent)

    # =========================
    # AGENT
    # =========================
    def handle_agent(self, text):
        if text.startswith("agent"):
            return self.agent.start(text)
        return None

    # =========================
    # EVOLVE
    # =========================
    def handle_evolve(self, text):
        if text.startswith("evolve"):
            parts = text.split(" ", 2)
            if len(parts) < 3:
                return "format: evolve <file> <instruction>"
            return self.revolver.evolve(parts[1], parts[2])
        return None

    # =========================
    # MAIN THINK ENGINE
    # =========================
    def think(self, text):
        intent = self.detect_intent(text)

        # CHAT
        if intent == "chat":
            res = self.chat(text)
            self.remember(text, res, "chat")
            return res

        # AGENT
        res = self.handle_agent(text)
        if res:
            self.remember(text, str(res), "agent")
            return res

        # EVOLVE
        res = self.handle_evolve(text)
        if res:
            self.remember(text, str(res), "evolve")
            return res

        # COMMAND AI
        cmds = self.cmd_ai.generate(text)

        last_error = ""

        for c in cmds:
            c = safe_command(c)
            if not c:
                continue

            try:
                result = engine.run(c)

                if result.get("success"):
                    out = f"⚙️ {c}\n{result['output']}"
                    self.remember(text, out, "command")
                    return out

                last_error = result.get("output")

            except Exception as e:
                last_error = str(e)

        fail = f"❌ gagal\n{last_error if last_error else 'no output'}"
        self.remember(text, fail, "error")
        return fail