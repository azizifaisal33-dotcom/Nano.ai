#!/usr/bin/env python3
"""
🧠 NANO AI v12 - CONTINUOUS EVOLUTION BRAIN
Self-expanding modular AI system (safe architecture removed restrictions but stable)
"""

import os
import subprocess
import importlib
import json
import shutil
from datetime import datetime


# ==========================
# 🧠 CORE BRAIN
# ==========================
class NanoBrain:

    def __init__(self):
        self.memory = []
        self.plugins = {}
        self.usage_stats = {}
        self.version = "v12"

        self.commands = {}
        self.register_commands()

        self.load_memory()
        self.load_plugins()

        print("\n🧠 NANO AI v12 EVOLUTION BRAIN")
        print("⚡ Self Growing AI + Memory + Plugins + Git\n")

    # ==========================
    # SHELL RUNNER
    # ==========================
    def run(self, cmd):
        return subprocess.getoutput(cmd)

    # ==========================
    # COMMAND SYSTEM
    # ==========================
    def register_commands(self):

        self.commands = {
            "ram": self.cmd_ram,
            "cpu": self.cmd_cpu,
            "disk": self.cmd_disk,
            "ip": self.cmd_ip,
            "help": self.cmd_help,
            "install": self.cmd_install,
            "update": self.cmd_update,
            "plugin": self.cmd_plugin,
            "analyze": self.cmd_analyze,
            "learn": self.cmd_learn,
            "stats": self.cmd_stats,
        }

    # ==========================
    # MEMORY SYSTEM
    # ==========================
    def load_memory(self):
        try:
            with open("memory.json", "r") as f:
                self.memory = json.load(f)
        except:
            self.memory = []

    def save_memory(self):
        try:
            with open("memory.json", "w") as f:
                json.dump(self.memory[-200:], f)
        except:
            pass

    # ==========================
    # PLUGINS
    # ==========================
    def load_plugins(self):
        for folder in ["core", "Plugins"]:
            if not os.path.exists(folder):
                continue

            for file in os.listdir(folder):
                if file.endswith(".py"):
                    name = f"{folder}.{file[:-3]}"
                    try:
                        self.plugins[name] = importlib.import_module(name)
                        print(f"📦 loaded: {name}")
                    except:
                        pass

    # ==========================
    # SYSTEM COMMANDS
    # ==========================
    def cmd_ram(self, args):
        return self.run("free -h")

    def cmd_cpu(self, args):
        return self.run("top -bn1 | head -10")

    def cmd_disk(self, args):
        return self.run("df -h")

    def cmd_ip(self, args):
        return self.run("ip addr")

    def cmd_help(self, args):
        return """
🧠 NANO AI v12

ram cpu disk ip
install <pkg>
plugin <name>
analyze
learn <skill>
stats
update
"""

    def cmd_install(self, args):
        return f"pkg install {args[0]}" if args else "install <pkg>"

    # ==========================
    # UPDATE SYSTEM
    # ==========================
    def cmd_update(self, args):
        print("🔄 git update...")

        self.backup()

        result = self.run("git pull origin main")

        if "Already up to date" not in result:
            os.execv("python", ["python", "brain.py"])

        return "ok"

    # ==========================
    # PLUGIN LOADER
    # ==========================
    def cmd_plugin(self, args):
        if not args:
            return "plugin <name>"

        name = args[0]

        try:
            mod = importlib.import_module(f"core.{name}")
            self.plugins[name] = mod
            return f"loaded {name}"
        except:
            return "not found"

    # ==========================
    # ANALYZE SYSTEM
    # ==========================
    def cmd_analyze(self, args):

        score = len(self.plugins) * 10 + len(self.memory) // 2

        return f"health {score}/100"

    # ==========================
    # LEARNING SYSTEM (NEW CORE)
    # ==========================
    def cmd_learn(self, args):

        if not args:
            return "learn <skill>"

        skill = args[0]

        file = f"core/auto_{skill}.py"

        code = f'''
# AUTO GENERATED MODULE
def run():
    return "skill {skill} active"
'''

        with open(file, "w") as f:
            f.write(code)

        return f"learned {skill}"

    # ==========================
    # STATS SYSTEM
    # ==========================
    def cmd_stats(self, args):

        return {
            "memory": len(self.memory),
            "plugins": len(self.plugins),
            "version": self.version
        }

    # ==========================
    # EVOLUTION TRACKING
    # ==========================
    def track(self, cmd):

        self.usage_stats[cmd] = self.usage_stats.get(cmd, 0) + 1

    # ==========================
    # REASON ENGINE (NEW CORE)
    # ==========================
    def reason(self, text):

        text = text.lower()
        self.track(text.split()[0] if text.split() else "none")

        parts = text.split()

        if parts and parts[0] in self.commands:
            return self.commands[parts[0]](parts[1:])

        # natural mapping
        if "ram" in text:
            return self.cmd_ram([])

        if "cpu" in text:
            return self.cmd_cpu([])

        if "disk" in text:
            return self.cmd_disk([])

        if "install" in text:
            return self.cmd_install([text.split()[-1]])

        if "update" in text:
            return self.cmd_update([])

        if "learn" in text:
            return self.cmd_learn([text.split()[-1]])

        return self.fallback(text)

    # ==========================
    # FALLBACK
    # ==========================
    def fallback(self, text):
        return f"unknown: {text}"

    # ==========================
    # BACKUP SYSTEM
    # ==========================
    def backup(self):
        folder = f"backup_{self.version}"

        if os.path.exists(folder):
            shutil.rmtree(folder)

        shutil.copytree(".", folder,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))

    # ==========================
    # MAIN LOOP
    # ==========================
    def start(self):

        print("\n🧠 v12 running\n")

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
                print("\nstop")
                break


# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    NanoBrain().start()