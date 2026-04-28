import uuid
import os

from core.command_ai import CommandAI
from core.agent import Agent
from core.revolver import Revolver
from core.memory import memory
from core.knowledge_builder import search_knowledge
from core.generator import NanoGenerator


# =========================
# SAFE SYSTEM
# =========================
class FileSystem:
    def read(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except: return None

    def write(self, path, content):
        try:
            os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except: return False

class Backup:
    def create(self):
        try:
            import shutil
            if os.path.exists("core/brain.py"):
                shutil.copy("core/brain.py", "core/brain_backup.py")
            return True
        except: return False

def safe_command(cmd):
    blacklist = ["rm -rf", "shutdown", "reboot", "sudo", "mkfs", "dd if=", "format"]
    return None if any(b in cmd.lower() for b in blacklist) else cmd


# =========================
# BRAIN CLASS (PROPER INDENTATION!)
# =========================
class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.agent = Agent(self)
        self.fs = FileSystem()
        self.backup = Backup()
        self.revolver = Revolver(self.fs, self.backup)
        self.generator = NanoGenerator()
        self.session_id = str(uuid.uuid4())[:8]
        print(f"🧠 Nano BRAIN v2.5 | Session: {self.session_id}")

    def chat(self, text):
        t = text.lower()
        if "halo" in t or "hai" in t:
            return "Yo bro! 👋 NanoAI siap bantu! 😎"
        if "siapa kamu" in t:
            return "Aku NanoAI - otak buatan sendiri dengan DNA evolution system! 🧬"
        if "apa yang bisa" in t or "kemampuan" in t:
            return """🤖 Kemampuan NanoAI:
🔫 evolve <file> <inst> - DNA code evolution
🤖 agent <goal> - AI autonomous agent
📊 status - Brain + DNA status
💬 Chat pintar & belajar otomatis"""
        if "help" in t:
            return "Ketik: evolve, agent, status, atau chat aja bro!"
        return f"Masih belajar nih bro: '{text}' 🤔"

    def think(self, text):  # ✅ PROPER INDENTATION!
        text = text.strip()
        if not text:
            return "Kosong bro, ketik sesuatu dong 😅"

        print(f"🧠 Thinking... ({text[:30]}...)")

        # 1. DNA EVOLUTION (PRIORITY #1)
        if text.lower().startswith("evolve"):
            parts = text.split(" ", 2)
            if len(parts) >= 3:
                return self.revolver.evolve(parts[1], parts[2])
            return "❌ Format: evolve <file.py> <instruction>"

        # 2. AGENT MODE
        if text.lower().startswith("agent"):
            return self.agent.start(text[6:].strip())

        # 3. STATUS
        if text.lower() in ["status", "info"]:
            return self.status()

        # 4. CHAT FALLBACK (BEFORE COMMANDS!)
        chat_resp = self.chat(text)
        if "belajar nih" not in chat_resp:
            return chat_resp

        # 5. KNOWLEDGE & MEMORY
        kb = search_knowledge(text)
        if kb:
            return f"📚 Knowledge: {kb}"

        mem = memory.search(text)
        if mem:
            return f"💾 Memory: {mem[0]['ai_response']}"

        # 6. COMMAND AI (LAST!)
        commands = self.cmd_ai.generate(text)
        safe_cmds = [safe_command(c) for c in commands if safe_command(c)]
        if safe_cmds:
            return f"💻 Saran command:\n" + "\n".join(f"  {i+1}. {c}" for i,c in enumerate(safe_cmds[:3]))

        # 7. GENERATOR
        return self.generator.reply(text)

    def status(self):
        try:
            return f"""🧠 BRAIN STATUS:
📱 Session: {self.session_id}
🔫 DNA: {self.revolver.status()}
💾 Memory: {len(memory.search(''))} records"""
        except:
            return "🧠 Brain ready!"

    def remember(self, user_input, ai_output, intent="chat"):
        try:
            memory.add(self.session_id, user_input, ai_output, intent)
        except:
            pass

# Global instance
brain = Brain()