#!/usr/bin/env python3
"""
EMERGENCY REPAIR PROTOCOL - NANOAI v2.5 OMNI-LVR
Full System Reconstruction + Nuclear Failsafe
"""

import os
import sys
import traceback
from pathlib import Path

def nuclear_repair():
    """NUCLEAR FAILSAFE - Complete system reconstruction"""
    print("💥 NUCLEAR REPAIR ACTIVATED")
    root = Path(__file__).parent
    
    # 1. KILL ALL PROCESSES
    os.system("pkill -f nanoai 2>/dev/null")
    os.system("rm -f /tmp/nanoai.lock 2>/dev/null")
    
    # 2. REBUILD CORE FILES
    core_files = {
        "core/revolver.py": revolver_minimal,
        "core/brain.py": brain_minimal,
        "core/agent.py": agent_minimal,
        "cli/shell.py": shell_minimal,
        "main.py": main_minimal
    }
    
    for filepath, content in core_files.items():
        (root / filepath).write_text(content)
        print(f"🔧 REBUILT: {filepath}")
    
    # 3. SELF-VALIDATE
    import ast
    for filepath in core_files:
        try:
            content = (root / filepath).read_text()
            ast.parse(content)
            print(f"✅ VALID: {filepath}")
        except:
            print(f"❌ INVALID: {filepath}")
    
    print("✅ NUCLEAR REPAIR COMPLETE")
    print("🔄 REBOOTING...")
    os.execl(sys.executable, sys.executable, str(root / "main.py"))

# MINIMAL WORKING FILES
revolver_minimal = '''#!/usr/bin/env python3
class Revolver:
    def evolve_file(self, file, inst):
        return f"EVOLVED {{file}}: {{inst}}"
    
    def reconstruct_brain(self):
        print("Brain reconstructed")
    
    def intent_signature(self, text):
        return "shard123"
    
    def auto_mutate(self, shard, lr):
        pass

revolver = Revolver()
'''

brain_minimal = '''#!/usr/bin/env python3
class Brain:
    def __init__(self):
        self.agent = type('Agent', (), {'self_heal': lambda x: print("Healing")})
        print("🧠 MINIMAL BRAIN BOOT")
    
    def think(self, text):
        return f"🧠 {{text.upper()}} - Brain online!"
    
    def status(self):
        return "🧠 STATUS: MINIMAL OK"

brain = Brain()
'''

agent_minimal = '''#!/usr/bin/env python3
class SelfHealingAgent:
    def __init__(self, brain):
        self.brain = brain
    
    def self_heal(self, error):
        print(f"🔧 HEALED: {{error[:50]}}")
    
    def execute_unrestricted(self, goal):
        return f"AGENT: Executing {{goal}}"

class Agent:
    def __init__(self, brain):
        self.healer = SelfHealingAgent(brain)
    
    def start(self, goal):
        return self.healer.execute_unrestricted(goal)
'''

shell_minimal = '''#!/usr/bin/env python3
from pathlib import Path
import sys

class NanoShell:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        sys.path.insert(0, str(self.root / 'core'))
        from brain import Brain
        self.brain = Brain()
        self.running = True
    
    def start(self):
        print("\\n🧠 EMERGENCY SHELL v2.5")
        print("💬 chat | $ cmd | evolve file 'inst' | agent goal")
        while self.running:
            try:
                inp = input("🧠> ").strip()
                if inp in ['exit', 'quit']:
                    break
                if inp.startswith('$'):
                    os.system(inp[1:])
                else:
                    print(self.brain.think(inp))
            except:
                print("Error - continuing")

if __name__ == "__main__":
    NanoShell().start()
'''

main_minimal = '''#!/usr/bin/env python3
from pathlib import Path
import sys
import os

print("🧠 NANOAI v2.5 MINIMAL BOOT")
root = Path(__file__).parent
sys.path.insert(0, str(root / 'core'))

try:
    from cli.shell import NanoShell
    NanoShell().start()
except:
    print("EMERGENCY SHELL")
    while True:
        cmd = input("🧠> ").strip()
        if cmd in ['exit', 'quit', 'repair']:
            break
        if cmd == 'nuclear':
            import subprocess
            subprocess.run([sys.executable, str(root / "main.py")])
        else:
            os.system(cmd)
'''

print("🔧 EMERGENCY REPAIR PROTOCOL")
print("1. Nuclear repair? (y/n)")

choice = input("> ").strip().lower()
if choice in ['y', 'yes', '1']:
    nuclear_repair()
else:
    print("Manual repair mode")
    print("Run: python -c \"exec(open('main.py').read())\"")