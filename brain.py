#!/usr/bin/env python3
"""
🧠 NANO AI v21 - SELF OPTIMIZING CORE
Priority engine + adaptive memory + performance loop
"""

import os
import time
import subprocess
import importlib
import json
import threading
from datetime import datetime


# ==========================
# 🧠 MAIN BRAIN
# ==========================
class NanoBrain:

    def __init__(self):
        self.memory = []
        self.plugins = {}
        self.task_queue = []
        self.running = True

        self.performance_log = {
            "tasks_done": 0,
            "tasks_failed": 0,
            "avg_time": 0
        }

        self.version = "v21"

        self.commands = {}
        self.register_commands()

        self.load_memory()
        self.load_plugins()

        self.worker = threading.Thread(target=self.background_loop)
        self.worker.daemon = True
        self.worker.start()

        print("\n🧠 NANO AI v21 SELF-OPTIMIZING CORE")
        print("⚡ Priority Engine + Adaptive Memory + Loop\n")

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
            "tasks": self.cmd_tasks,
            "status": self.cmd_status,
            "memory": self.cmd_memory,
            "optimize": self.cmd_optimize,
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
        json.dump(self.memory[-600:], open("memory.json","w"))

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
    # PLANNER (WITH PRIORITY)
    # ==========================
    def cmd_plan(self, args):

        task = " ".join(args)

        priority = self.calculate_priority(task)

        plan = {
            "task": task,
            "steps": [
                "analyze",
                "execute",
                "verify"
            ],
            "priority": priority,
            "status": "queued",
            "created": str(datetime.now())
        }

        self.task_queue.append(plan)

        self.sort_tasks()

        return plan

    # ==========================
    # PRIORITY ENGINE
    # ==========================
    def calculate_priority(self, task):

        score = 0

        if "error" in task or "fix" in task:
            score += 5

        if "install" in task:
            score += 3

        if "github" in task:
            score += 2

        return score

    def sort_tasks(self):

        self.task_queue.sort(key=lambda x: x["priority"], reverse=True)

    # ==========================
    # RUN TASK
    # ==========================
    def cmd_run(self, args):

        if not self.task_queue:
            return "no tasks"

        task = self.task_queue.pop(0)

        start = time.time()

        results = []

        try:
            for step in task["steps"]:
                results.append(self.safe_execute(step))

            task["status"] = "done"
            self.performance_log["tasks_done"] += 1

        except:
            task["status"] = "failed"
            self.performance_log["tasks_failed"] += 1

        end = time.time()

        self.update_avg_time(end - start)

        return results

    # ==========================
    # TASK LIST
    # ==========================
    def cmd_tasks(self, args):
        return self.task_queue

    # ==========================
    # MEMORY SEARCH (WEIGHTED)
    # ==========================
    def cmd_memory(self, args):

        if not args:
            return "memory <query>"

        q = args[0]

        scored = []

        for m in self.memory:
            weight = m.get("weight", 1)
            if q in m["input"]:
                scored.append((weight, m))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [m for w, m in scored[:5]]

    # ==========================
    # STATUS
    # ==========================
    def cmd_status(self, args):

        return {
            "version": self.version,
            "memory": len(self.memory),
            "plugins": len(self.plugins),
            "tasks": len(self.task_queue),
            "performance": self.performance_log
        }

    # ==========================
    # AUTO OPTIMIZE ENGINE
    # ==========================
    def cmd_optimize(self, args):

        avg = self.performance_log["avg_time"]

        if avg > 2:
            suggestion = "reduce subprocess calls"
        else:
            suggestion = "system stable"

        return {
            "avg_time": avg,
            "suggestion": suggestion
        }

    # ==========================
    # SAFE EXECUTION
    # ==========================
    def safe_execute(self, step):

        blacklist = ["rm", "dd", "shutdown"]

        for b in blacklist:
            if b in step:
                return "blocked"

        return f"executed: {step}"

    # ==========================
    # PERFORMANCE TRACKING
    # ==========================
    def update_avg_time(self, new_time):

        old = self.performance_log["avg_time"]

        self.performance_log["avg_time"] = (old + new_time) / 2

    # ==========================
    # BACKGROUND LOOP (OPTIMIZER)
    # ==========================
    def background_loop(self):

        while self.running:

            # auto re-sort tasks
            self.sort_tasks()

            # adaptive memory weighting
            for m in self.memory[-50:]:
                m["weight"] = m.get("weight", 1) + 0.1

            time.sleep(3)

    # ==========================
    # REASON ENGINE
    # ==========================
    def reason(self, text):

        parts = text.lower().split()

        if parts and parts[0] in self.commands:
            return self.commands[parts[0]](parts[1:])

        if "plan" in text:
            return self.cmd_plan(parts[1:])

        if "run" in text:
            return self.cmd_run([])

        return f"unknown: {text}"

    # ==========================
    # MAIN LOOP
    # ==========================
    def start(self):

        print("\n🧠 v21 READY (self-optimizing)\n")

        while self.running:
            try:
                user = input("nano> ")

                if user in ["exit", "quit"]:
                    self.running = False
                    break

                out = self.reason(user)
                print(out)

                self.memory.append({
                    "input": user,
                    "output": str(out),
                    "time": str(datetime.now()),
                    "weight": 1
                })

                self.save_memory()

            except KeyboardInterrupt:
                self.running = False
                break


# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    NanoBrain().start()