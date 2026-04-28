
#!/usr/bin/env python3
"""
🧠 NanoAI - Complete AI Brain System
DNA-Powered Evolution Engine
"""

import os
from core.brain import Brain
from core.revolver import Revolver  # ✅ FIXED IMPORT
from core.memory import memory
from core.fs import FileSystem  # Assuming you have this
from cli.shell import NanoShell

class FileSystem:
    def read(self, path): 
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except: return None
    
    def write(self, path, content):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except: return False

class Backup:
    def create(self):
        try:
            import shutil
            shutil.copy("core/brain.py", "core/brain_backup.py")
            return True
        except: return False

class NanoAI:
    def __init__(self):
        self.fs = FileSystem()
        self.backup = Backup()
        self.brain = Brain()
        self.revolver = Revolver(self.fs, self.backup)  # ✅ FIXED CLASS NAME
        
        print("🚀 NanoAI FULLY LOADED")
        print("🧬 DNA Evolution Active")

    def start_shell(self):
        shell = NanoShell(self.brain)
        shell.start()

    def evolve(self, file_path, instruction):
        return self.revolver.evolve(file_path, instruction)

    def status(self):
        return self.brain.status() + f"\n🔫 {self.revolver.status()}"

# Global instance
nano = NanoAI()