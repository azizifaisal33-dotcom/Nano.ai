#!/usr/bin/env python3
"""
🧠 NANO AI v2 + TERMUX ENCYCLOPEDIA (FIXED VERSION)
"""

import subprocess
from datetime import datetime


class TermuxBrain:
    def __init__(self):
        self.memory = []
        print("🧠 NANO AI + TERMUX BRAIN LOADED!")
        print("💾 Ready for Termux commands")

    # SAFE RUN COMMAND
    def run_cmd(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip() if result.stdout else result.stderr.strip()
        except:
            return "❌ Command error"

    # TERMUX KNOWLEDGE
    def get_termux_knowledge(self, query):
        query = query.lower()

        if "ram" in query:
            return f"📊 RAM:\n{self.run_cmd('free -h')}"

        if "cpu" in query:
            return f"⚙️ CPU:\n{self.run_cmd('top -bn1 | head -15')}"

        if "disk" in query:
            return f"💾 Disk:\n{self.run_cmd('df -h')}"

        if "ip" in query:
            return f"🌐 IP:\n{self.run_cmd('ip addr')}"

        if "uptime" in query:
            return f"⏱ Uptime:\n{self.run_cmd('uptime')}"

        return None

    # PACKAGE GUIDE
    def package_guide(self, pkg):
        packages = {
            "python": "pkg install python python-pip",
            "git": "pkg install git",
            "node": "pkg install nodejs",
            "curl": "pkg install curl",
            "wget": "pkg install wget",
        }
        return packages.get(pkg, f"pkg search {pkg}")

    # TROUBLESHOOT
    def troubleshoot(self, text):
        if "no module" in text:
            return "pip install <module>"
        if "permission denied" in text:
            return "termux-setup-storage"
        if "not found" in text:
            return "pkg install <command>"
        return "Coba: pkg update && pkg upgrade"

    # MAIN LOGIC
    def think(self, text):
        text = text.strip().lower()
        time = datetime.now().strftime("%H:%M:%S")

        # SYSTEM KNOWLEDGE
        knowledge = self.get_termux_knowledge(text)
        if knowledge:
            response = knowledge

        # INSTALL COMMAND
        elif "install" in text:
            pkg = text.split()[-1]
            response = f"🔧 Install:\n{self.package_guide(pkg)}"

        # ERROR HANDLING
        elif "error" in text or "gagal" in text:
            response = f"🔧 Fix:\n{self.troubleshoot(text)}"

        # HELP
        elif "help" in text:
            response = f"""
🧠 TERMUX BRAIN HELP

📦 install python git node
📊 cek ram | cek cpu | cek disk
🌐 ip | uptime
❓ error fix otomatis
"""

        # GREETING
        elif any(x in text for x in ["halo", "hai", "hello"]):
            response = f"🤖 Halo! Nano AI aktif ({time})"

        else:
            response = f"🤖 Unknown: {text}\n💡 coba help"

        self.memory.append((text, response))
        return response


def main():
    print("\n🧠 NANO AI TERMUX BRAIN STARTED\n")

    brain = TermuxBrain()

    while True:
        try:
            user = input("\nnano> ")

            if user.lower() in ["exit", "quit"]:
                print("👋 Bye!")
                break

            if not user:
                continue

            result = brain.think(user)
            print(result)

        except KeyboardInterrupt:
            print("\n👋 Stop")
            break


if __name__ == "__main__":
    main()