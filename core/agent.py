#!/usr/bin/env python3
import os
import sys
import traceback
import subprocess
from pathlib import Path
from core.revolver import get_revolver  # Lazy import

class SelfHealingAgent:
    def __init__(self, brain=None):
        self.brain = brain
        self.revolver = get_revolver()
        self.history = []
        self.error_count = 0
        self.max_errors = 3

    def execute_safely(self, command: str) -> str:
        """Execute with full error recovery"""
        try:
            if command.startswith("agent "):
                return self._agent_mode(command[6:])
            return self.brain.think(command) if self.brain else "No brain"
        except Exception as e:
            self.error_count += 1
            error_trace = traceback.format_exc()
            return self._self_heal(error_trace, command)

    def _self_heal(self, error_trace: str, failed_command: str) -> str:
        """Full self-repair cycle"""
        print(f"💥 Error #{self.error_count}: {error_trace.splitlines()[0]}")
        
        if self.error_count >= self.max_errors:
            return self._emergency_reboot()
        
        # 1. Analyze error
        error_file = self._extract_file_from_trace(error_trace)
        if not error_file or not Path(error_file).exists():
            return "Cannot self-repair missing file"
        
        # 2. Internet fix + repair
        fix_result = self.revolver.self_repair(error_trace, error_file)
        
        # 3. Test repair
        try:
            result = self.brain.think(failed_command) if self.brain else "Repaired"
            self.error_count = 0  # Reset on success
            return f"{fix_result}\n🔄 Retry: {result}"
        except:
            return f"Repair failed. Manual intervention needed."

    def _extract_file_from_trace(self, trace: str) -> str:
        """Parse traceback for file"""
        for line in trace.splitlines():
            if "File " in line and ".py" in line:
                return line.split('"')[1]
        return "core/brain.py"  # Default

    def _emergency_reboot(self) -> str:
        """Nuclear option: regenerate core"""
        print("☢️ EMERGENCY REBOOT")
        try:
            # Regen all core files
            core_dir = Path("core")
            for core_file in ["brain.py", "agent.py", "revolver.py"]:
                if not (core_dir / core_file).exists():
                    (core_dir / core_file).write_text("# Regenerated\npass")
            
            # Restart python
            os.execl(sys.executable, sys.executable, *sys.argv)
        except:
            return "Reboot failed. System compromised."

    def _agent_mode(self, goal: str) -> str:
        """Autonomous agent execution"""
        steps = goal.split(" && ")
        results = []
        
        for step in steps:
            step = step.strip()
            if step.startswith("pip install"):
                subprocess.Popen(["pip", "install"] + step.split()[2:])
                results.append("📦 Installing...")
            elif step.startswith("curl") or step.startswith("wget"):
                os.system(step)
                results.append(f"🌐 {step}")
            else:
                result = self.brain.think(step) if self.brain else step
                results.append(result)
        
        return "\n".join(results)

    def status(self) -> str:
        return f"🛠️ Errors: {self.error_count}/{self.max_errors} | History: {len(self.history)}"

class Agent:
    def __init__(self, brain):
        self.brain = brain
        self.agent = SelfHealingAgent(brain)

    def start(self, goal: str):
        return self.agent.execute_safely(f"agent {goal}")

# Global agent
agent = Agent(None)  # Brain injected later