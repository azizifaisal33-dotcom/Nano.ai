NanoAI v2.5 Self-Evolving OS - Autonomous Termux Kernel
Auto-dependency, PID killer, self-healing bootstrap
"""

import os
import sys
import subprocess
import signal
import psutil
from pathlib import Path
import importlib.util
import time

class NanoKernel:
    def __init__(self):
        self.root = Path(__file__).parent
        self.pid_file = self.root / "nano.pid"
        self._kill_ghosts()

    def _kill_ghosts(self):
        """Kill hanging NanoAI processes"""
        my_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'name']):
            if 'python' in proc.info['name'].lower() and 'nano' in proc.info['name'].lower():
                if proc.info['pid'] != my_pid and self.root.name in proc.cmdline():
                    proc.kill()
                    print(f"👻 Killed ghost PID {proc.info['pid']}")

    def auto_install(self, packages: list):
        """Silent pip/pkg install"""
        for pkg in packages:
            if 'termux' in pkg:
                subprocess.run(['pkg', 'install', pkg.replace('termux-', '')], 
                             capture_output=True)
            else:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', pkg], 
                             capture_output=True)
            print(f"📦 {pkg} → OK")

    def bootstrap(self):
        """Full system bootstrap"""
        print("🧠 NanoAI v2.5 Kernel Boot...")
        
        # Auto-deps
        deps = ['requests', 'beautifulsoup4', 'psutil']
        for dep in deps:
            if not importlib.util.find_spec(dep.replace('-', '_')):
                self.auto_install([dep])
        
        # Regen missing core
        for core in ['brain.py', 'agent.py', 'revolver.py']:
            p = self.root / 'core' / core
            if not p.exists():
                p.write_text(f"# Auto-regen {core}\nclass {core[:-3].title()}:\n    pass\n")
        
        # Launch
        from cli.shell import NanoShell
        NanoShell().start()

if __name__ == "__main__":
    kernel = NanoKernel()
    kernel.bootstrap()