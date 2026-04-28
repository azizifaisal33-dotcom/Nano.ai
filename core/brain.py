import uuid
import os
import subprocess

from core.command_ai import CommandAI
from core.agent import Agent
from core.revolver import Revolver
from core.engine import engine
from core.memory import memory
from core.knowledge_builder import search_knowledge, add_knowledge
from core.generator import NanoGenerator


# =========================
# SAFE SYSTEM
# =========================
class FileSystem:

def think(self, text):
    text = text.strip()
    if not text: return "Kosong nih 😅"

    print(f"🧠 Thinking... ({text[:30]}...)")

    # 1. DNA EVOLUTION FIRST (REVOLVER)
    if text.lower().startswith("evolve"):
        parts = text.split(" ", 2)
        if len(parts) >= 3:
            return self.revolver.evolve(parts[1], parts[2])
        return "Format: evolve <file> <instruction>"

    # 2. AGENT MODE
    if text.lower().startswith("agent"):
        return self.agent.start(text[6:].strip())

    # 3. KNOWLEDGE + MEMORY (BEFORE COMMAND!)
    kb = search_knowledge(text)
    if kb: return f"📚 {kb}"
    
    mem = memory.search(text)
    if mem: return f"💾 {mem[0]['ai_response']}"

    # 4. CHAT FALLBACK (BEFORE COMMAND AI!)
    chat_response = self.chat(text)
    if "belum paham" not in chat_response.lower():
        return chat_response

    # 5. COMMAND AI (LAST RESORT)
    commands = self.cmd_ai.generate(text)
    safe_cmds = [safe_command(c) for c in commands if safe_command(c)]
    if safe_cmds:
        return f"💻 Saran:\n" + "\n".join(f"  {i+1}. {c}" for i,c in enumerate(safe_cmds[:3]))

    # 6. GENERATOR
    return self.generator.reply(text)

    def read(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return None

    def write(self, path, content):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except:
            return False


class Backup:
    def create(self):
        try:
            import shutil
            shutil.copy("core/brain.py", "core/brain_backup.py")
            return True
        except:
            return False


def safe_command(cmd):
    blacklist = ["rm -rf", "shutdown", "reboot", "sudo", "mkfs", "dd if=", "format"]
    cmd_lower = cmd.lower()
    return None if any(b in cmd_lower for b in blacklist) else cmd


# =========================
# BRAIN CORE
# =========================
class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.agent = Agent(self)

        # dependency injection
        self.fs = FileSystem()
        self.backup = Backup()
        self.revolver = Revolver(self.fs, self.backup)

        # generator AI
        self.generator = NanoGenerator()

        self.session_id = str(uuid.uuid4())[:8]
        
        # create data dir
        os.makedirs("data/memory", exist_ok=True)
        
        print("🧠 Nano AI BRAIN v2.5 ONLINE")
        print(f"📱 Session: {self.session_id}")

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
        if "halo" in t or "hai" in t:
            return "Halo 👋 Aku NanoAI - AI buatan sendiri untuk Termux!"
        if "siapa kamu" in t:
            return "Aku NanoAI v2.5 - Brain AI 100% pure Python untuk Android/Termux"
        if "siapa aku" in t:
            return "Kamu adalah master NanoAI! Coba ketik 'help' untuk command"
        if "help" in t:
            return """📋 QUICK COMMANDS:
agent <goal>     - AI Agent mode
evolve <file> <inst> - Code evolution
status          - Brain status
lihat file      - List files"""
        return "🤔 Belum paham, tapi aku belajar dari setiap input kamu!"

    # =========================
    # MAIN THINK ENGINE (FIXED!)
    # =========================
    def think(self, text):
        text = text.strip()
        if not text:
            return "Kosong nih, ketik sesuatu dong 😅"

        print(f"🧠 Thinking... ({text[:50]}...)")

        # =========================
        # 1. AUTO LEARNING
        # =========================
        self.generator.train(text)

        # =========================
        # 2. KNOWLEDGE BASE
        # =========================
        kb = search_knowledge(text)
        if kb:
            self.remember(text, kb, "knowledge")
            return f"📚 Knowledge: {kb}"

        # =========================
        # 3. MEMORY SEARCH
        # =========================
        mem = memory.search(text)
        if mem:
            res = mem[0]["ai_response"]
            self.remember(text, res, "memory")
            return f"💾 Memory: {res}"

        # =========================
        # 4. AGENT MODE
        # =========================
        if text.lower().startswith("agent "):
            goal = text[6:].strip()
            res = self.agent.start(goal)
            self.remember(text, str(res), "agent")
            return res

        # =========================
        # 5. EVOLVE MODE
        # =========================
        if text.lower().startswith("evolve "):
            parts = text.split(" ", 2)
            if len(parts) < 3:
                return "❌ Format: evolve <file.py> <instruction>"
            file_path, instruction = parts[1], parts[2]
            self.backup.create()
            res = self.revolver.evolve(file_path, instruction)
            self.remember(text, str(res), "evolve")
            return res

        # =========================
        # 6. SYSTEM COMMANDS
        # =========================
        if text.lower() == "status":
            return self.status()
        if text.lower() == "clear":
            os.system('clear' if os.name == 'posix' else 'cls')
            return "🧹 Screen cleared!"

        # =========================
        # 7. COMMAND AI
        # =========================
        commands = self.cmd_ai.generate(text)
        safe_cmds = [safe_command(cmd) for cmd in commands if safe_command(cmd)]
        if safe_cmds:
            result = f"💻 Saran command:\n" + "\n".join(f"  {i+1}. {cmd}" for i, cmd in enumerate(safe_cmds[:5]))
            self.remember(text, result, "command")
            return result

        # =========================
        # 8. GENERATOR FALLBACK
        # =========================
        fallback = self.generator.reply(text)
        self.remember(text, fallback, "generator")
        return fallback

    # =========================
    # UTILITY METHODS
    # =========================
    def status(self):
        stats = memory.stats()
        return f"""📊 BRAIN STATUS:
🆔 Session: {self.session_id}
💾 Memory: {stats['total_records']} records
🤖 Generator: {len(self.generator.chain)} chains
⚙️  Ready for action!"""

    def clear_memory(self):
        memory.clear()
        return "🧹 Memory dibersihkan (fresh start!)"

# Global instance for compatibility
brain = Brain()