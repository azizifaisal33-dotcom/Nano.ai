"""
🧠 Nano AI v2 Core - Neural Brain Framework
"""
__version__ = "2.0.0"
__author__ = "Nano AI Team"

from .tokenizer import NanoTokenizer
from .vector import NanoVectorStore
from .intent import NanoIntentEngine
from .memory import NanoMemory
from .generator import NanoGenerator
from .nano import NanoAI

__all__ = [
    "NanoTokenizer", "NanoVectorStore", "NanoIntentEngine",
    "NanoMemory", "NanoGenerator", "NanoAI"
]

# Auto-init data directory
import os
os.makedirs("data", exist_ok=True)
print("🧠 Nano AI v2 Core loaded")