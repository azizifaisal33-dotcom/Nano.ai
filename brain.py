#!/usr/bin/env python3
"""
🧠 NANO AI v28 - CONVERSATION FLOW CORE
Context state + follow-up understanding + dialogue flow
"""

import os
import json
import subprocess
import importlib
from datetime import datetime


# ==========================
# 🧠 MAIN BRAIN
# ==========================
class NanoBrain:

    def __init__(self):
        self.memory = []
        self.plugins = {}
        self.task_queue = []

        self.version = "v28"

        # GRAPH + LANGUAGE (from previous versions)
        self.graph = {}

        # 🧠 CONVERSATION STATE (NEW CORE)
        self.conversation_history = []
        self.current_topic = None

        self.basic_knowledge = {
            "siapa": "identitas",
            "apa": "penjelasan",
            "kenapa": "alasan",
            "kamu": "AI",
            "aku": "user",
            "halo": "sapaan"
        }

        self.commands = {}
        self.register_commands()

        self.load_memory()
        self.load_plugins()

        print("\n🧠 NANO AI v28 CONVERSATION FLOW CORE")
        print("⚡ Context State + Dialogue Flow Engine\n")

    # ==========================
    # SHELL
    # ==========================
    def run(self, cmd):
        return subprocess.getoutput(cmd)

    # ==========================
    # COMMANDS
    # ==========================
    def register_commands(self):

        self.commands = {
            "plan": self.cmd_plan,
            "run": self.cmd_run,
            "memory": self.cmd_memory,
            "status": self.cmd_status,
        }

    # ==========================
    # MEMORY
    # ==========================
    def load_memory(self):
        try:
            self.memory = json.load(open("memory.json"))
        except:
            self.memory = []

    def save_memory(self):
        json.dump(self.memory[-1000:], open("memory.json","w"))

    # ==========================
    # PLUGINS
    # ==========================
    def load_plugins(self):

        self.plugins = {}

        for folder in ["core", "Plugins"]:
            if not os.path.exists(folder):
                continue

            for file in os.listdir(folder):
                if file.endswith(".py"):
                    module = f"{folder}.{file[:-3]}"

                    try:
                        self.plugins[module] = importlib.import_module(module)
                    except:
                        pass

        print(f"🔌 plugins: {len(self.plugins)}")

    # ==========================
    # BASIC COMMANDS
    # ==========================
    def cmd_plan(self, args):
        task = " ".join(args)

        self.task_queue.append({
            "task": task,
            "status": "queued"
        })

        return f"planned: {task}"

    def cmd_run(self, args):
        if not self.task_queue:
            return "no tasks"

        task = self.task_queue.pop(0)
        return f"executed: {task['task']}"

    def cmd_memory(self, args):
        if not args:
            return "memory <query>"

        q = args[0]

        return [m for m in self.memory if q in m["input"]][-5:]

    def cmd_status(self, args):
        return {
            "version": self.version,
            "memory": len(self.memory),
            "plugins": len(self.plugins),
            "tasks": len(self.task_queue),
            "topic": self.current_topic
        }

    # ==========================
    # 🧠 UPDATE CONTEXT STATE
    # ==========================
    def update_context(self, text):

        self.conversation_history.append(text)

        # keep last 5 messages only
        self.conversation_history = self.conversation_history[-5:]

        # detect topic
        words = text.lower().split()

        for w in words:
            if w in self.basic_knowledge:
                self.current_topic = w

    # ==========================
    # 🧠 FOLLOW-UP DETECTION
    # ==========================
    def is_follow_up(self, text):

        follow_words = ["itu", "lanjut", "jelaskan", "terus", "lagi"]

        return any(w in text.lower() for w in follow_words)

    # ==========================
    # 🧠 CONTEXT ANALYSIS
    # ==========================
    def get_context(self):

        if not self.conversation_history:
            return None

        return self.conversation_history[-2:]

    # ==========================
    # 🧠 RESPONSE ENGINE
    # ==========================
    def generate_response(self, text):

        self.update_context(text)

        # GREETING
        if "halo" in text.lower():
            return "👋 Halo! Aku Nano AI v28 dengan conversation flow."

        # FOLLOW UP HANDLING (NEW CORE)
        if self.is_follow_up(text):

            ctx = self.get_context()

            if ctx:
                return (
                    "🧠 Aku melanjutkan percakapan sebelumnya:\n"
                    f"- {ctx[-1]}\n\n"
                    "💡 Aku akan mencoba menjelaskan lebih lanjut."
                )

            return "🤖 Aku belum tahu konteks sebelumnya."

        # QUESTION
        if "apa" in text.lower() or "siapa" in text.lower():

            if self.current_topic:
                return f"🧠 Kamu menanyakan tentang '{self.current_topic}', aku akan menjelaskan itu."

            return "🤖 Itu pertanyaan, tapi aku butuh konteks lebih."

        # DEFAULT
        return self.smart_fallback(text)

    # ==========================
    # 🧠 SWARM (still kept)
    # ==========================
    def swarm(self, text):

        return {
            "planner": f"[Planner] {text}",
            "analyst": f"[Analyst] {text}",
            "executor": f"[Executor] {text}"
        }

    # ==========================
    # FALLBACK
    # ==========================
    def smart_fallback(self, text):

        if len(text.split()) < 3:
            return "🤖 coba jelaskan lebih panjang"

        return "🤖 aku masih mencoba memahami konteks percakapan ini"

    # ==========================
    # REASON ENGINE
    # ==========================
    def reason(self, text):

        parts = text.lower().split()

        if parts and parts[0] in self.commands:
            return self.commands[parts[0]](parts[1:])

        return self.generate_response(text)

    # ==========================
    # MAIN LOOP
    # ==========================
    def start(self):

        print("\n🧠 v28 READY (conversation flow active)\n")

        while True:
            try:
                user = input("nano> ")

                if user in ["exit", "quit"]:
                    break

                out = self.reason(user)
                print(out)

                self.memory.append({
                    "input": user,
                    "output": str(out),
                    "time": str(datetime.now())
                })

                self.save_memory()

            except KeyboardInterrupt:
                break


# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    NanoBrain().start()