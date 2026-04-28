import uuid

from core.command_ai import CommandAI
from core.agent import Agent
from core.revolver import Revolver
from core.engine import engine
from core.memory import memory
from core.knowledge_builder import search_knowledge, add_knowledge


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
    # MEMORY WRAPPER
    # =========================
    def remember(self, user, ai, intent):
        memory.add(self.session_id, user, ai, intent=intent)

    # =========================
    # CHAT ENGINE (FALLBACK LOGIC)
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
    # THINK ENGINE (3 LAYER SYSTEM)
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
        # [2] MEMORY LAYER (HISTORY)
        # =========================
        mem = memory.search(text)
        if mem:
            response = mem[0]["ai_response"]
            self.remember(text, response, "memory")
            return response

        # =========================
        # [3] CHAT LOGIC
        # =========================
        if text.startswith("agent"):
            res = self.agent.start(text)
            self.remember(text, str(res), "agent")
            return res

        if text.startswith("evolve"):
            parts = text.split(" ", 2)
            if len(parts) < 3:
                return "format: evolve <file> <instruction>"
            res = self.revolver.evolve(parts[1], parts[2])
            self.remember(text, str(res), "evolve")
            return res

        # =========================
        # COMMAND AI
        # =========================
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
                    add_knowledge(text, result["output"])  # AUTO LEARN
                    return out

                last_error = result.get("output")

            except Exception as e:
                last_error = str(e)

        # =========================
        # CHAT FALLBACK
        # =========================
        res = self.chat(text)
        self.remember(text, res, "chat")
        add_knowledge(text, res)  # AUTO LEARN CHAT
        return res