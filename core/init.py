"""
🧠 Nano AI v2 Core - Neural Brain Framework
"""
__version__ = "2.0.0"
__author__ = "Nano AI Team"

# Lazy imports - Avoid circular dependency
def get_tokenizer():
    from .tokenizer import NanoTokenizer
    return NanoTokenizer()

def get_vectorstore():
    from .vector import NanoVectorStore
    return NanoVectorStore()

def get_intent_engine():
    from .intent import NanoIntentEngine
    return NanoIntentEngine()

def get_memory():
    from .memory import NanoMemory
    return NanoMemory()

def get_generator():
    from .generator import NanoGenerator
    return NanoGenerator()

def get_nano_ai():
    from .nano import NanoAI
    return NanoAI()

# Public API
__all__ = [
    "get_tokenizer", "get_vectorstore", "get_intent_engine",
    "get_memory", "get_generator", "get_nano_ai"
]

# Auto-init
import os
os.makedirs("data", exist_ok=True)
print("🧠 Nano AI v2 Core loaded ✓")