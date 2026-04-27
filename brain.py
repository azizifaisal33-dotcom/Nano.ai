#!/usr/bin/env python3
"""
🧠 NANO AI v33 - ABJAD + CHARACTER REASONING CORE
Letter-level understanding + language decomposition
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

        self.version = "v33"

        self.conversation_history = []

        # 5W1H (v29+)
        self.w5h_map = {
            "apa": "WHAT",
            "siapa": "WHO",
            "kenapa": "WHY",
            "kapan": "WHEN",
            "dimana": "WHERE",
            "bagaimana": "HOW"
        }

        # KNOWLEDGE BASE (v32)
        self.knowledge_base = {
            "python": "bahasa pemrograman AI dan automation",
            "ai": "kecerdasan buatan",
            "termux": "terminal linux di android"
        }

        self.learned_knowledge = {}

        self.commands = {}
        self.register_commands()

        self.load_memory()
        self.load_plugins()

        print("\n🧠 NANO AI v33 ABJAD CORE")
        print("⚡ Character-Level Understanding Active\n")

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
        json.dump(self.memory[-1200:], open("memory.json","w"))

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
            "learned": len(self.learned_knowledge)
        }

    # ==========================
    # 🧠 ABJAD CORE (NEW)
    # ==========================
    def analyze_letters(self, text):

        letters = list(text.lower())

        vowels = "aiueo"
        v = [c for c in letters if c in vowels]
        c = [c for c in letters if c.isalpha() and c not in vowels]

        return {
            "text": text,
            "letters": letters,
            "vowels": v,
            "consonants": c,
            "length": len(letters)
        }

    # ==========================
    # 🧠 WORD BREAKDOWN (NEW CORE)
    # ==========================
    def word_decomposition(self, text):

        words = text.split()

        result = []

        for w in words:
            result.append({
                "word": w,
                "chars": list(w),
                "count": len(w)
            })

        return result

    # ==========================
    # CONTEXT
    # ==========================
    def update_context(self, text):
        self.conversation_history.append(text)
        self.conversation_history = self.conversation_history[-5:]

    # ==========================
    # 5W1H
    # ==========================
    def detect_5w1h(self, text):

        text = text.lower()

        for k in self.w5h_map:
            if k in text:
                return self.w5h_map[k]

        return None

    # ==========================
    # KNOWLEDGE LOOKUP
    # ==========================
    def knowledge_lookup(self, text):

        text = text.lower()

        for k in self.knowledge_base:
            if k in text:
                return self.knowledge_base[k]

        for k in self.learned_knowledge:
            if k in text:
                return self.learned_knowledge[k]

        return None

    # ==========================
    # RESPONSE ENGINE (UPGRADED)
    # ==========================
    def generate_response(self, text):

        self.update_context(text)

        text_l = text.lower()

        # GREETING
        if "halo" in text_l:
            return "👋 Halo! Aku Nano AI v33 dengan abjad reasoning."

        # 🧠 ABJAD REQUEST DETECT
        if "abjad" in text_l or "huruf" in text_l:

            analysis = self.analyze_letters(text)

            return (
                "🧠 ABJAD ANALYSIS:\n"
                f"- Huruf: {analysis['letters']}\n"
                f"- Vokal: {analysis['vowels']}\n"
                f"- Konsonan: {analysis['consonants']}\n"
                f"- Total: {analysis['length']}"
            )

        # WORD BREAKDOWN MODE
        if "kata" in text_l or "pecah" in text_l:

            return {
                "decomposition": self.word_decomposition(text)
            }

        # 5W1H
        if self.detect_5w1h(text):
            return self.knowledge_lookup(text) or "🧠 butuh data tambahan"

        # KNOWLEDGE
        kb = self.knowledge_lookup(text)
        if kb:
            return f"🧠 PENJELASAN:\n{kb}"

        return "🤖 aku masih belajar memahami kata ini"

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

        print("\n🧠 v33 READY (abjad reasoning active)\n")

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