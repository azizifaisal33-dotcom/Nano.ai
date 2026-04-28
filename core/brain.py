import uuid
import os

from core.command_ai import CommandAI
from core.agent import Agent
from core.revolver import Revolver
from core.engine import engine
from core.memory import memory
from core.knowledge_builder import search_knowledge, add_knowledge
from core.generator import generator


# =========================
# SAFE SYSTEM
# =========================
class FileSystem:
    def read(self, path):
        if not os.path.exists(path): return None
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def write(self, path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


class Backup:
    def create(self, source="core/brain.py"):
        try:
            target = source.replace(".py", "_backup.py")
            os.system(f"cp {source} {target}")
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
        
        # 1. Siapkan System Tools dulu
        self.fs = FileSystem()
        self.backup = Backup()
        
        # 2. Inject ke Revolver (DNA System)
        # Sesuai perbaikan: Revolver(fs, backup, path)
        self.revolver = Revolver(self.fs, self.backup, dna_path="data/brain.lvr")

        # 3. Agent & Generator
        self.agent = Agent(self)
        self.generator = generator

        self.session_id = str(uuid.uuid4())[:10]
        print("🧠 Nano AI BRAIN ONLINE")

    # =========================
    # MEMORY SYSTEM
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
        if "halo" in t: return "Halo 👋 aku NanoAI"
        if "siapa kamu" in t: return "Aku NanoAI system kamu"
        if "siapa aku" in t: return "Aku belum tahu kamu siapa"
        
        # Gunakan generator murni kamu jika tidak ada kecocokan chat manual
        return self.generator.reply(text)

    # =========================
    # THINK ENGINE
    # =========================
    def think(self, text):
        text = text.strip().lower()

        # =========================
        # 0. AUTO LEARNING
        # =========================
        self.generator.train(text)

        # =========================
        # 1. KNOWLEDGE LAYER (Database Teks)
        # =========================
        kb = search_knowledge(text)
        if kb:
            self.remember(text, kb, "knowledge")
            return kb

        # =========================
        # 2. MEMORY LAYER (SQLite)
        # =========================
        mem = memory.search(text)
        if mem:
            # Pastikan mengambil respons dari hasil search
            res = mem["ai_response"] if isinstance(mem, list) else None
            if res:
                self.remember(text, res, "memory")
                return res

        # =========================
        # 3. AGENT MODE
        # =========================
        if text.startswith("agent "):
            goal = text.replace("agent ", "", 1)
            res = self.agent.start(goal)
            self.remember(text, str(res), "agent")
            return res

        # =========================
        # 4. EVOLVE MODE (Revolver)
        # =========================
        if text.startswith("evolve"):
            parts = text.split(" ", 2)
            if len(parts) < 3:
                return "Format: evolve <file> <instruction>"
            
            # Update DNA berdasarkan instruksi
            # Kita pecah instruksi jadi tokens untuk revolver
            self.revolver.evolve(parts.split())
            
            res = f"🧬 Evolution applied to {parts} using DNA weights."
            self.remember(text, res, "evolve")
            return res

        # =========================
        # 5. COMMAND AI (Terminal)
        # =========================
        cmds = self.cmd_ai.generate(text)
        if cmds and cmds != text:
            res = f"Saran perintah: {', '.join(cmds)}"
            self.remember(text, res, "command")
            return res

        # =========================
        # 6. FINAL FALLBACK
        # =========================
        return self.chat(text)
