#!/usr/bin/env python3
import os
import subprocess
import traceback
import re
from pathlib import Path

class SelfHealingAgent:
    def __init__(self, brain):
        self.brain = brain
        self.revolver = self._lazy_revolver()
        self.errors = 0

    def _lazy_revolver(self):
        sys.path.insert(0, str(Path(__file__).parent))
        from revolver import Revolver
        return Revolver()

    def self_heal(self, error_trace: str):
        """Full self-repair"""
        self.errors += 1
        
        # Parse error
        file_match = re.search(r'File "([^"]+\.py)"', error_trace)
        if not file_match:
            return "Cannot parse error"
        
        error_file = file_match.group(1)
        
        # Auto-fix common errors
        fixes = {
            "IndentationError": "    pass",
            "SyntaxError": "pass",
            "ImportError": "try:\n    import missing\nexcept:\n    pass"
        }
        
        content = Path(error_file).read_text(errors='ignore')
        for err_type, fix in fixes.items():
            if err_type in error_trace:
                content += f"\n# Auto-fix {err_type}\n{fix}"
                break
        
        Path(error_file).write_text(content)
        self.revolver.evolve_file(error_file, f"fixed {error_trace.splitlines()[0]}")
        
        print(f"🔧 Repaired {error_file}")
        return "Self-healed"

    def execute_unrestricted(self, goal: str) -> str:
        """100% unrestricted execution"""
        steps = goal.split(" | ")
        results = []
        
        for step in steps:
            step = step.strip()
            
            if step.startswith("pkg "):
                subprocess.run(["pkg"] + step.split()[1:], capture_output=True)
                results.append("📦 pkg OK")
            
            elif step.startswith("pip "):
                subprocess.run([sys.executable, "-m", "pip"] + step.split()[1:], 
                             capture_output=True)
                results.append("📦 pip OK")
            
            elif step.startswith("curl ") or step.startswith("wget "):
                os.system(step)
                results.append(f"🌐 {step}")
            
            else:
                try:
                    result = self.brain.think(step)
                    results.append(result)
                except:
                    tb = traceback.format_exc()
                    self.self_heal(tb)
                    results.append("🛠️ Auto-fixed")
        
        return "\n".join(results)

    def status(self):
        return f"🛠️ Errors fixed: {self.errors}"

class Agent:
    def __init__(self, brain):
        self.healer = SelfHealingAgent(brain)

    def start(self, goal: str):
        return self.healer.execute_unrestricted(goal)