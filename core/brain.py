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
        "rm -rf", "shutdown", "reboot",
        "sudo", "mkfs", "dd if="
    ]
    return None if any(b in cmd for b in blacklist) else cmd


# =========================
# DEPENDENCY WRAPPER
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
# BRAIN CORE
# =========================
class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.agent = Agent(self)

        # FIX: always inject dependency
        self.revolver = Revolver(FileSystem(), Backup())

        self.session_id = str(uuid.uuid4())[:10]

        print("🧠 Nano AI BRAIN ONLINE")

    # =========================
    # MEMORY SAVE
    # =========================
    def remember(self, user, ai, intent="chat"):
        try:
            memory.add(self.session_id, user, ai, intent=intent)
        except Exception:
            pass

    # =========================
    # FALLBACK CHAT
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
    # THINK ENGINE (CORE FLOW)
    # =========================
    def think(self, text):
        text = text.strip().lower()

        # -------------------------
        # 1. KNOWLEDGE LAYER
        # -------------------------
        kb = search_knowledge(text)
        if kb:
            self.remember(text, kb, "knowledge")
            return kb

        # -------------------------
        # 2. MEMORY LAYER
        # -------------------------
        try:
            mem = memory.search(text)
            if mem and "ai_response" in mem[0]:
                response = mem[0]["ai_response"]
                self.remember(text, response, "memory")
                return response
        except Exception:
            pass

        # -------------------------
        # 3. AGENT MODE
        # -------------------------
        if text.startswith("agent"):
            res = self.agent.start(text)
            self.remember(text, str(res), "agent")
            return res

        # -------------------------
        # 4. EVOLVE MODE
        # -------------------------
        if text.startswith("evolve"):
            parts = text.split(" ", 2)
            if len(parts) < 3:
                return "format: evolve <file> <instruction>"

            res = self.revolver.evolve(parts[1], parts[2])
            self.remember(text, str(res), "evolve")
            return res

        # -------------------------
        # 5. COMMAND AI EXECUTION
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
                    self.remember(text, output, "command")

                    # auto learning
                    try:
                        add_knowledge(text, result["output"])
                    except:
                        pass

                    return output

                last_error = result.get("output")

            except Exception as e:
                last_error = str(e)

        # -------------------------
        # 6. CHAT FALLBACK
        # -------------------------
        res = self.chat(text)
        self.remember(text, res, "chat")

        try:
            add_knowledge(text, res)
        except:
            pass

        return res