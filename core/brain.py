import os
import sys
import uuid
import json

# FIX PATH IMPORT (WAJIB)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.command_ai import CommandAI
from core.agent import Agent
from core.revolver import Revolver
from core.engine import engine
from core.memory import memory


# =========================
# SAFE COMMAND FILTER
# =========================
def safe_command(cmd):
    blacklist = [
        "rm -rf",
        "shutdown",
        "reboot",
        "git push",
        "git pull",
        "sudo",
        "mkfs",
        "dd if="
    ]

    for b in blacklist:
        if b in cmd.lower():
            return None

    return cmd


# =========================
# MAIN BRAIN
# =========================
class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.agent = Agent(self)
        self.revolver = Revolver()

        self.session_id = str(uuid.uuid4())[:12]

        # learning system
        self.learn_cache = []

        print("🧠 NanoAI FINAL EVOLVED SYSTEM READY")
        print(f"📦 Session: {self.session_id}")


    # =========================
    # CONTEXT MEMORY
    # =========================
    def get_context(self, text, limit=5):
        try:
            history = memory.search(text, session_id=self.session_id, limit=limit)
        except:
            history = memory.history(self.session_id, limit)

        context = []
        for h in history:
            context.append(f"user: {h['user_input']}")
            context.append(f"ai: {h['ai_response']}")

        return "\n".join(context)


    # =========================
    # LEARNING SYSTEM
    # =========================
    def learn_patterns(self):
        if len(self.learn_cache) < 5:
            return

        try:
            if os.path.exists("data/learning.json"):
                with open("data/learning.json", "r") as f:
                    patterns = json.load(f)
            else:
                patterns = {}

            for item in self.learn_cache:
                key = item["input"]

                if key not in patterns:
                    patterns[key] = []

                if item["output"]:
                    patterns[key].append(item["output"])

            with open("data/learning.json", "w") as f:
                json.dump(patterns, f)

            self.learn_cache = []

        except:
            pass


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
    # EVOLVE MODE
    # =========================
    def handle_evolve(self, text):
        if text.startswith("evolve"):
            parts = text.split(" ", 2)

            if len(parts) < 3:
                return "format: evolve <file> <instruksi>"

            return self.revolver.evolve(parts[1], parts[2])

        return None


    # =========================
    # THINK ENGINE (FULL AI CORE)
    # =========================
    def think(self, text):
        text_clean = text.strip().lower()

        # =========================
        # SAVE INPUT
        # =========================
        memory.add(
            session_id=self.session_id,
            user_input=text_clean,
            ai_response="",
            intent="input"
        )

        # =========================
        # CONTEXT MEMORY
        # =========================
        context = self.get_context(text_clean)

        # =========================
        # AGENT
        # =========================
        res = self.handle_agent(text_clean)
        if res:
            memory.add(self.session_id, text_clean, res, intent="agent")

            self.learn_cache.append({
                "input": text_clean,
                "output": res,
                "success": True
            })

            return res

        # =========================
        # EVOLVE
        # =========================
        res = self.handle_evolve(text_clean)
        if res:
            memory.add(self.session_id, text_clean, res, intent="evolve")

            self.learn_cache.append({
                "input": text_clean,
                "output": res,
                "success": True
            })

            return res

        # =========================
        # LEARNING RECALL (PATTERN MEMORY)
        # =========================
        try:
            if os.path.exists("data/learning.json"):
                with open("data/learning.json") as f:
                    patterns = json.load(f)

                if text_clean in patterns and len(patterns[text_clean]) > 0:
                    return patterns[text_clean][0]
        except:
            pass

        # =========================
        # COMMAND AI (WITH CONTEXT)
        # =========================
        enhanced_input = f"""
Context:
{context}

User:
{text_clean}
"""

        cmds = self.cmd_ai.generate(enhanced_input)

        last_error = ""
        output_final = None

        for c in cmds:
            c = safe_command(c)

            if not c:
                continue

            try:
                result = engine.run(c)

                if result.get("success"):
                    output_final = f"⚙