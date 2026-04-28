
import os

class NanoConfig:
    def __init__(self):
        self.AGENT_NAME = "NanoAI"
        self.OWNER_NAME = "Yeshie"
        self.VERSION = "2.0-STABLE-LOCAL"
        
        self.LOCAL_HOST = "127.0.0.1"
        self.LOCAL_PORT = "11434"
        self.ENDPOINT = f"http://{self.LOCAL_HOST}:{self.LOCAL_PORT}/api/chat"
        self.AI_MODEL = "qwen2:1.5b"
        
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.SYSTEM_DATA = os.path.join(self.ROOT_DIR, "data", "memory", "system.json")

    def get_core_instruction(self):
        return (
            f"Role: {self.AGENT_NAME}. User: {self.OWNER_NAME}. "
            "Expertise: Android Dev (Sketchware Pro), Firebase, Bash, Linux. "
            "Style: Casual, smart, technical, Indonesian."
        )

config = NanoConfig()
