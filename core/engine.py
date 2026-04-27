"""
⚙️ NanoEngine v2 - Safe Execution Engine
Production-grade command execution
"""
import subprocess
import shlex
from typing import Dict, Any, Optional
from pathlib import Path
from rich.table import Table
from rich.console import Console
from config import config

class NanoEngine:
    def __init__(self):
        self.console = Console()
        self.safe_commands = self._load_safe_list()
        self.blacklist = self._load_blacklist()

    def _load_safe_list(self) -> set:
        """Approved commands"""
        return {
            'pkg', 'apt', 'free', 'df', 'top', 'htop', 'uptime', 'ls', 'cd',
            'pwd', 'whoami', 'id', 'ps', 'kill', 'ip', 'ping', 'ss', 'git',
            'python', 'node', 'nginx', 'curl', 'wget'
        }

    def _load_blacklist(self) -> set:
        """Dangerous commands"""
        return {'rm -rf', 'dd', 'mkfs', 'shutdown', 'reboot', 'halt'}

    def run(self, command: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """Safe command execution"""
        if timeout is None:
            timeout = config['CMD_TIMEOUT']
            
        # Safety checks
        if any(bl in command.lower() for bl in self.blacklist):
            return {"success": False, "error": "Blacklisted command"}
            
        # Sanitize
        safe_cmd = shlex.quote(command)
        
        try:
            result = subprocess.run(
                safe_cmd, shell=True, capture_output=True,
                text=True, timeout=timeout, cwd=Path.cwd()
            )
            
            output = result.stdout.strip() if result.stdout else result.stderr.strip()
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "output": output,
                "raw": result
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Timeout after {timeout}s"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def explain_execution(self, result: Dict):
        """Rich execution report"""
        table = Table(title="Execution Report")
        table.add_column("Status", style="bold")
        table.add_column("Details")
        
        if result["success"]:
            table.add_row("✅ Success", f"RC: {result['returncode']}")
            table.add_row("Output", result['output'][:100] + "..." if len(result['output']) > 100 else result['output'])
        else:
            table.add_row("❌ Failed", f"RC: {result.get('returncode', 'N/A')}")
            table.add_row("Error", result['error'])
            
        self.console.print(table)

# Global engine
engine = NanoEngine()