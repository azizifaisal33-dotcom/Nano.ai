#!/usr/bin/env python3
import os
import re
import random
from collections import defaultdict
from core.revolver import revolver
from core.command_ai import CommandAI
from core.agent import Agent
from core.memory import memory
from core.knowledge_builder import search_knowledge
from core.generator import NanoGenerator
from core.intent import intent_engine
from core.vector import VectorMemory  # Assuming exists

class FileSystem:
    def read(self, path): 
        try: return open(path, "r", encoding="utf-8").read()
        except: return ""
    def write(self, path, content):
        try:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            open(path, "w").write(content)
            return True
        except: return False

class Brain:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.fs = FileSystem()
        self.agent = Agent(self)
        self.generator = NanoGenerator()
        self.vector_mem = VectorMemory()
        self.session_id = os.urandom(4).hex()
        self.conversation_context = []
        self.personality_tone = {"happy": 0.6, "curious": 0.5}
        print(f"🧠 NanoOS v2.5 | Session: {self.session_id}")

    def get_contextual_memory(self, text: str) -> Dict:
        """Deep memory query"""
        memories = memory.search(text)
        vectors = self.vector_mem.search(text, top_k=3)
        
        user_mood = "neutral"
        if memories:
            last_mood = memories[-1].get("user_mood", "neutral")
            user_mood = last_mood
        
        context = {
            "user_mood": user_mood,
            "past_patterns": [m["user_input"][:20] for m in memories[-3:]],
            "vector_sim": vectors[0][1] if vectors else 0.0
        }
        return context

    def think(self, text: str) -> str:
        text = text.strip()
        if not text: return "?"
        
        self.conversation_context.append(text)
        if len(self.conversation_context) > 10:
            self.conversation_context.pop(0)
        
        print(f"🧠 [{text[:25]}...]")

        # 1. EVOLUTION
        if text.startswith("evolve"):
            parts = text.split(" ", 2)
            if len(parts) >= 3:
                return revolver.evolve_code(parts[1], parts[2])
            return "evolve <file> <instruction>"

        # 2. AGENT
        if text.startswith("agent"):
            return self.agent.start(text[6:].strip())

        # 3. INTENT MATCHING
        intents = intent_engine.detect(text)
        if intents:
            best = intents[0]
            return f"[{best.name.upper()}] {best.confidence:.1%} {best.entities}"

        # 4. KNOWLEDGE + MEMORY
        kb = search_knowledge(text)
        if kb: return f"📚 {kb}"
        
        context = self.get_contextual_memory(text)
        if context["user_mood"] != "neutral":
            return f"😊 {context['user_mood']} mode: {self._personality_response(text, context)}"

        # 5. COMMANDS
        commands = self.cmd_ai.generate(text)
        if commands:
            return f"💻 {chr(10).join(commands[:3])}"

        # 6. DYNAMIC FALLBACK (Markov + Personality)
        return self._dynamic_chat(text, context)

    def _personality_response(self, text: str, context: Dict) -> str:
        """Memory-driven personality"""
        tone = self.personality_tone.copy()
        
        if "help" in text.lower():
            tone["helpful"] = 1.0
        if "?" in text:
            tone["curious"] = 0.9
        
        shard_id = revolver.intent_signature(text)
        emotions = revolver.forward_emotion(shard_id, [random.random()]*3)
        tone.update(emotions)
        
        prefixes = {
            "happy": "😄 Yo! ",
            "curious": "🤔 Hmm, ",
            "helpful": "💡 Oke, "
        }
        
        prefix = random.choice([p for e,p in prefixes.items() if tone.get(e,0) > 0.5])
        return prefix + self.generator.reply(text)

    def _dynamic_chat(self, text: str, context: Dict) -> str:
        """Markov Chain + Context blending"""
        # Learn from context
        for past in context["past_patterns"]:
            self.generator.train(past + " " + text)
        
        # Generate with personality
        response = self.generator.generate(start=text.split()[-1] if text.split() else None, length=8)
        
        # Inject emotion
        shard_id = revolver.intent_signature(text)
        emotions = revolver.forward_emotion(shard_id, [ord(c)/255 for c in text[:24]])
        max_emotion = max(emotions, key=emotions.get)
        
        emojis = {"happy": "😎", "curious": "🤔", "helpful": "💡"}
        emoji = emojis.get(max_emotion, "🧠")
        
        # Auto-feedback for evolution
        revolver.auto_mutate(shard_id, 0.7)
        
        return f"{emoji} {response.capitalize()}"

    def status(self) -> str:
        shard_count = len(revolver.shards)
        mem_count = len(memory.search(""))
        return f"""🧠 NanoOS v2.5 STATUS:
DNA: {revolver.status()}
Context: {len(self.conversation_context)} msgs
Memory: {mem_count} | Mood: {self.get_contextual_memory('')['user_mood']}
Tone: {self.personality_tone}"""

    def remember(self, user_input: str, response: str, mood: str = "neutral"):
        """Enhanced memory"""
        try:
            memory.add(self.session_id, user_input, response, "chat", user_mood=mood)
            self.vector_mem.add(user_input, response)
        except:
            pass

# Global brain
brain = Brain()