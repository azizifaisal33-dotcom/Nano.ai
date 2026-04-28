#!/usr/bin/env python3
"""
CLI/SHELL.PY - ZERO-BYPASS COGNITIVE INTERFACE
Indestructible Command Routing + Self-Correcting Brain
"""

import os
import sys
import traceback
import re
from pathlib import Path

class NanoShell:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.brain = self._load_brain()
        self.running = True
        self.history = []
        self.command_mode = "chat"  # chat | system | agent | evolve
    
    def _load_brain(self):
        """Zero-bypass brain loader with reconstruction"""
        sys.path.insert(0, str(self.root / 'core'))
        
        try:
            from brain import Brain
            return Brain()
        except:
            print("🧠 EMERGENCY RECONSTRUCT")
            from revolver import Revolver
            rev = Revolver()
            rev.reconstruct_brain()
            from brain import Brain
            return Brain()
    
    def _route_command(self, user_input: str) -> str:
        """Strict Zero-Bypass routing logic"""
        user_input = user_input.strip()
        
        # SYSTEM COMMANDS (highest priority)
        if user_input.lower() in ['exit', 'quit', 'bye']:
            self.running = False
            return "👋 DNA preserved"
        
        if user_input.startswith('$'):
            return self._exec_system(user_input[1:])
        
        if user_input.startswith('evolve '):
            return self._exec_evolve(user_input[7:])
        
        if user_input.startswith('agent '):
            return self._exec_agent(user_input[6:])
        
        # FALLBACK: Pure cognitive processing
        return self.brain.think(user_input)
    
    def _exec_system(self, cmd: str) -> str:
        """Raw system execution"""
        try:
            result = os.popen(cmd).read()
            return result.strip() or "OK"
        except Exception as e:
            return f"💥 System error: {e}"
    
    def _exec_evolve(self, instruction: str) -> str:
        """Self-editing evolution"""
        try:
            from revolver import Revolver
            rev = Revolver()
            parts = instruction.split(" ", 1)
            if len(parts) >= 2:
                return rev.evolve_file(parts[0], parts[1])
            return "evolve <file> <instruction>"
        except:
            return "🛠️ Evolution failed - self-repairing"
    
    def _exec_agent(self, goal: str) -> str:
        """Agent execution"""
        try:
            from agent import Agent
            agent = Agent(self.brain)
            return agent.execute_unrestricted(goal)
        except:
            return "🛠️ Agent failed - reconstructing"
    
    def start(self):
        os.system('clear')
        print("🧠 NANOAI v2.5 OMNI-LVR COGNITIVE SHELL")
        print("💬 chat | $ system | evolve file 'inst' | agent goal")
        print("=" * 70)
        
        while self.running:
            try:
                user_input = input("🧠 ").strip()
                if not user_input:
                    continue
                
                self.history.append(user_input)
                
                result = self._route_command(user_input)
                print(result)
                
                # Auto-feedback loop
                if "error" in result.lower() or "failed" in result.lower():
                    print("🔄 SELF-CORRECTING...")
                    self.brain.agent.self_heal(traceback.format_exc())
                
            except KeyboardInterrupt:
                print("\n⏹️ Interrupted")
                break
            except Exception as e:
                tb = traceback.format_exc()
                print(f"💥 CRASH: {e}")
                self.brain.agent.self_heal(tb)

if __name__ == "__main__":
    NanoShell().start()