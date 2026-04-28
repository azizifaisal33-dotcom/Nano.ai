import uuid

from core.command_ai import CommandAI
from core.agent import Agent
from core.revolver import Revolver
from core.engine import engine
from core.memory import memory
from core.knowledge_builder import search_knowledge, add_knowledge


# =========================
# SAFE SYSTEM
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
            import os
            os.system("cp core/brain.py core/brain_backup.py")
        except:
            pass


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

        # FIX IMPORTANT (dependency injection)
        self.fs = FileSystem()
        self.backup = Backup()
        self.revolver = Revolver(self.fs, self.backup)

        self.session_id = str(uuid.uuid4())[:10]

        print("🧠 Nano AI BRAIN ONLINE")

    # =========================
    # MEMORY
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
    # CHAT FALLBACK
    # =========================
    def chat(self, text):
        t = text.lower()

        if "halo" in t:
            return "Halo 👋 aku NanoAI"

        if "siapa kamu" in t:
            return "Aku NanoAI system kamu"

        if "siapa aku" in t:
            return "Aku belum tahu kamu siapa"

        return "Aku belum paham, tapi aku belajar 🤖"

    # =========================
    # THINK ENGINE
    # =========================
    def think(self, text):
        text = text.strip().lower()

        # =========================
        # 1. KNOWLEDGE LAYER
        # =========================
        kb = search_knowledge(text)
        if kb:
            self.remember(text, kb, "knowledge")
            return kb

        # =========================
        # 2. MEMORY LAYER
        # =========================
        mem = memory.search(text)
        if mem:
            res = mem[0]["ai_response"]
            self.remember(text, res, "memory")
            return res

        # =========================
        # 3. AGENT MODE
        # =========================
        if text.startswith("agent"):
            res = self.agent.start(text)
            self.remember(text, str(res), "agent")
            return res

        # =========================
        # 4. EVOLVE MODE
        # =========================
        if text.startswith("evolve"):
            parts = text.split(" ", 2)
            if len(parts) < 3:
                return "format: evolve <file> <instruction>"
            res = self.revolver.evolve(parts[1], parts[2])
            self.remember(text, str(res), "evolve")
            return res

        # =========================
        # 5. COMMAND EXECUTION
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
                    output = f"⚙️ {c}\n{result['output']}"
                    self.remember(text, output, "command")
                    add_knowledge(text, result["output"])
                    return output

                last_error = result.get("output")

            except Exception as e:
                last_error = str(e)

        # =========================
        # 6. CHAT FALLBACK
        # =========================
        res = self.chat(text)
        self.remember(text, res, "chat")
        add_knowledge(text, res)
        return res