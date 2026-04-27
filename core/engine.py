from config import config
import subprocess
import os


class Engine:
    def run(self, cmd):
        """
        cmd = string command dari AI system
        """

        # contoh simple executor (aman)
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip() or result.stderr.strip()
            }

        except Exception as e:
            return {
                "success": False,
                "output": str(e)
            }


engine = Engine()