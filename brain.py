#!/usr/bin/env python3
"""
🧠 NANO AI FULL PROJECT (SINGLE FILE VERSION)
- Agent System
- Memory Engine
- Vector Search
- Intent System
- Command AI
- Plugin Simulator
- CLI Runner
"""

import os
import json
import math
import subprocess
from datetime import datetime

# =========================
# MEMORY CORE (memory.py)
# =========================
class Memory:
    def __init__(self):
        self.data = []
        self.load()

    def load(self):
        try:
            self.data = json.load(open("memory.json"))
        except:
            self.data = []

    def save(self):
        json.dump(self.data[-2000:], open("memory.json","w"))

    def add(self, inp, out):
        self.data.append({
            "input": inp,
            "output": out,
            "time": str(datetime.now())
        })
        self.save()

# =========================
# TOKENIZER (tokenizer.py)
# =========================
class Tokenizer:
    def encode(self, text):
        return text.lower().split()

# =========================
# VECTOR ENGINE (vector.py)
# =========================
class VectorEngine:
    def embed(self, text):
        vec = {}
        for w in text.lower().split():
            vec[w] = vec.get(w, 0) + 1
        return vec

    def cosine(self, a, b):
        keys = set(a) | set(b)

        dot = sum(a.get(k,0)*b.get(k,0) for k in keys)
        ma = math.sqrt(sum(v*v for v in a.values()))
        mb = math.sqrt(sum(v*v for v in b.values()))

        if ma == 0 or mb == 0:
            return 0

        return dot / (ma * mb)

# =========================
# INTENT SYSTEM (intent.py)
# =========================
class Intent:
    def detect(self, text):
        text = text.lower()

        if "halo" in text:
            return "greeting"

        if "hitung" in text or "calc" in text:
            return "calc"

        if "memory" in text:
            return "memory"

        return "chat"

# =========================
# COMMAND AI (command_ai.py)
# =========================
class CommandAI:
    def run(self, cmd):
        return subprocess.getoutput(cmd)

# =========================
# AGENT (agent.py)
# =========================
class Agent:
    def __init__(self):
        self.memory = Memory()
        self.vector = VectorEngine()
        self.intent = Intent()
        self.tokenizer = Tokenizer()
        self.cmd = CommandAI()

    # SEARCH MEMORY
    def search(self, query):
        qv = self.vector.embed(query)

        best = None
        best_score = 0

        for item in self.memory.data:
            iv = self.vector.embed(item["input"])
            score = self.vector.cosine(qv, iv)

            if query in item["input"]:
                score += 0.2

            if score > best_score:
                best_score = score
                best = item["output"]

        if best_score > 0.3:
            return best

        return None

    # GENERATOR
    def generate(self, text):
        return f"🧠 Nano AI memahami: {text}"

    # MAIN PIPELINE
    def run(self, text):

        intent = self.intent.detect(text)

        # GREETING
        if intent == "greeting":
            return "👋 Halo, saya Nano AI Full Project"

        # CALC TOOL
        if intent == "calc":
            try:
                return str(eval(text.replace("hitung","")))
            except:
                return "error"

        # MEMORY SEARCH
        mem = self.search(text)
        if mem:
            return mem

        # GENERATE
        out = self.generate(text)

        self.memory.add(text, out)

        return out

# =========================
# PLUGIN SYSTEM (simulasi Plugins/)
# =========================
class PluginSystem:
    def __init__(self):
        self.plugins = {}

    def load(self):
        # simulasi plugin
        self.plugins["network"] = "active"
        self.plugins["system"] = "active"
        self.plugins["tts"] = "active"
        self.plugins["voice"] = "active"

# =========================
# REPL (cli/runner.py)
# =========================
class CLI:
    def __init__(self):
        self.agent = Agent()
        self.plugins = PluginSystem()
        self.plugins.load()

    def run(self):
        print("\n🧠 NANO AI FULL PROJECT (SINGLE FILE)")
        print("⚡ Agent + Memory + Vector + Intent System\n")

        while True:
            q = input("nano> ")

            if q in ["exit","quit"]:
                break

            print(self.agent.run(q))

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    CLI().run()