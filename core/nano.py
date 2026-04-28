#!/usr/bin/env python3
"""
🧠 NanoAI - 100% Self-Contained (No external deps!)
DNA-Powered Evolution Engine
"""

import os
import shutil
from core.brain import Brain
from core.revolver import Revolver
from cli.shell import NanoShell

# =========================
# INLINE FILESYSTEM (NO core.fs needed!)
# =========================
class FileSystem:
    def read(self, path): 
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except: 
            return None
    
    def write(self, path, content):
        try:
            os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except: 
            return False

class Backup:
    def create(self):
        try:
            if os.path.exists("core/brain.py"):
                shutil.copy("core/brain.py", "core/brain_backup.py")
            return True
        except: 
            return False

# =========================
# MAIN NANOAI CLASS
# =========================
class NanoAI:
    def __init__(self):
        self.fs = FileSystem()
        self.backup = Backup()
        self.brain = Brain()
        self.revolver = Revolver(self.fs, self.backup)
        
        print("🚀 NanoAI FULLY LOADED ✓")
        print("🧬 DNA Evolution Active ✓")
        print("💾 Self-contained (0 external deps) ✓")

    def start_shell(self):
        shell = NanoShell(self.brain)
        shell.start()

    def evolve(self, file_path, instruction):
        return self.revolver.evolve(file_path, instruction)

    def status(self):
        return self.brain.status() + f"\n🔫 {self.revolver.status()}"

    def dna_repair(self):
        return self.revolver.auto_repair()

# =========================
# GLOBAL INSTANCE
# =========================
nano = NanoAI()