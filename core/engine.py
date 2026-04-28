import os

class NanoConfig:
    def __init__(self):
        self.AGENT_NAME = "NanoAI"
        self.OWNER_NAME = "Yeshie"
        
        self.MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
        self.USE_SAFETENSORS = True
        
        self.CONTEXT_WINDOW = 2048
        self.MAX_NEW_TOKENS = 512
        self.TEMPERATURE = 0.7
        
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DB_PATH = os.path.join(self.ROOT_DIR, "data", "memory", "system.json")

    def get_system_prompt(self):
        return (
            f"Role: {self.AGENT_NAME}. Owner: {self.OWNER_NAME}. "
            "Expertise: Android (Sketchware Pro), Bash, Firebase. "
            "Style: Technical, casual, concise."
        )

config = NanoConfig()
