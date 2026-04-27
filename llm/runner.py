import subprocess

class LLMRunner:
    def __init__(self, model_path):
        self.model_path = model_path

    def generate(self, prompt):
        cmd = [
            "./llama.cpp/main",
            "-m", self.model_path,
            "-p", prompt
        ]

        result = subprocess.getoutput(" ".join(cmd))
        return result