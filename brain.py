#!/usr/bin/env python3
"""
🧠 NANO AI v26 - MULTI AGENT SWARM CORE
Planner + Analyst + Executor voting system
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

        self.version = "v26"

        # GRAPH + LEARNING (from v24-v25)
        self.graph = {}
        self.learning_log = {"good": 0, "bad": 0, "avg_score": 0}

        self.commands = {}
        self.register_commands()

        self.load_memory()
        self.load_plugins()

        print("\n🧠 NANO AI v26 SWARM CORE")
        print("⚡ Multi-Agent + Voting System\n")

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
            "swarm": self.cmd_swarm_test,
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
        json.dump(self.memory[-900:], open("memory.json","w"))

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
            "learning": self.learning_log
        }

    # ==========================
    # 🧠 AGENTS (NEW CORE)
    # ==========================

    def agent_planner(self, text):
        return f"[Planner] task breakdown: {text} -> steps generated"

    def agent_analyst(self, text):
        return f"[Analyst] interpreting: {text} -> meaning extracted"

    def agent_executor(self, text):
        return f"[Executor] executing logic for: {text}"

    # ==========================
    # 🧠 SWARM SYSTEM (VOTING)
    # ==========================
    def swarm(self, text):

        responses = [
            self.agent_planner(text),
            self.agent_analyst(text),
            self.agent_executor(text)
        ]

        # simple voting: longest + most detailed wins
        best = max(responses, key=lambda x: len(x))

        return {
            "all": responses,
            "best": best
        }

    # ==========================
    # 🧠 GRAPH UPDATE
    # ==========================
    def update_graph(self, text):

        words = text.lower().split()

        for w in words:
            if w not in self.graph:
                self.graph[w] = set()

            for o in words:
                if o != w:
                    self.graph[w].add(o)

    # ==========================
    # 🧠 RESPONSE ENGINE
    # ==========================
    def generate_response(self, text):

        if "halo" in text.lower():
            return "👋 Halo, aku Nano AI v26 Swarm Brain"

        if "apa kamu" in text.lower():
            return "🧠 Aku multi-agent AI dengan planner, analyst, executor"

        return None

    # ==========================
    # 🧠 REASON ENGINE (UPDATED)
    # ==========================
    def reason(self, text):

        self.update_graph(text)

        parts = text.lower().split()

        if parts and parts[0] in self.commands:
            return self.commands[parts[0]](parts[1:])

        # SWARM MODE (NEW CORE)
        swarm_result = self.swarm(text)

        base_response = self.generate_response(text)

        if base_response:
            return base_response

        return (
            "🧠 SWARM ANALYSIS:\n"
            f"- Planner: {swarm_result['all'][0]}\n"
            f"- Analyst: {swarm_result['all'][1]}\n"
            f"- Executor: {swarm_result['all'][2]}\n\n"
            f"🏆 BEST: {swarm_result['best']}"
        )

    # ==========================
    # SWARM TEST COMMAND
    # ==========================
    def cmd_swarm_test(self, args):

        text = " ".join(args)

        return self.swarm(text)

    # ==========================
    # MAIN LOOP
    # ==========================
    def start(self):

        print("\n🧠 v26 READY (multi-agent swarm)\n")

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