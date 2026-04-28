#!/usr/bin/env python3
import os
import sys
import traceback
from pathlib import Path

class NanoShell:
    def __init__(self, brain=None):
        self.root = Path(__file__).parent.parent
        self.brain = self._load_brain(brain)
        self.running = True
        self.history = []

    def _load_brain(self, brain):
        """Self-repairing brain loader"""
        try:
            sys.path.insert(0, str(self.root / 'core'))
            from brain import Brain
            return Brain()
        except:
            print("🧠 Brain repair mode...")
            from revolver import Revolver
            rev = Revolver()
            rev.evolve_file("core/brain.py", "basic brain class")
            from brain import Brain
            return Brain()

    def start(self):
        os.system('clear')
        print("🧠 NanoAI v2.5 Cognitive Shell")
        print("💬 Chat | $ command | agent goal | evolve file 'inst'")
        print("=" * 60)

        while self.running:
            try:
                user_input = input("🧠 ").strip()
                if not user_input:
                    continue
                
                self.history.append(user_input)
                
                # Cognitive Routing
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("👋 DNA preserved")
                    break
                
                if user_input.startswith('$'):
                    # Raw shell
                    result = os.popen(user_input[1:]).read()
                    print(result or "OK")
                
                elif user_input.startswith(('evolve', 'agent')):
                    # System commands
                    result = self.brain.think(user_input)
                    print(result)
                
                else:
                    # Pure chat → brain
                    result = self.brain.think(user_input)
                    print(result)
                
            except KeyboardInterrupt:
                print("\n⏹️ Interrupted")
                break
            except Exception as e:
                tb = traceback.format_exc()
                print(f"💥 {e}")
                self.brain.agent.self_heal(tb) if hasattr(self.brain, 'agent') else None

    def status(self):
        return f"History: {len(self.history)} | Brain: {getattr(self.brain, 'session_id', 'OK')}"

if __name__ == "__main__":
    NanoShell().start()