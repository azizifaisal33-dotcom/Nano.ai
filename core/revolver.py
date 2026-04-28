#!/usr/bin/env python3
import os
import pickle
import hashlib
import time
import random
import math
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class CognitiveShard:
    intent: str
    weights: List[float]  # Neural weights
    biases: List[float]   # Neural biases
    tone: Dict[str, float]  # Emotional tone {happy:0.8, serious:0.3}
    context_patterns: List[str]  # Conversation patterns
    activation_count: int = 0
    success_count: int = 0
    mutation_count: int = 0
    last_mutated: float = 0.0

class CognitiveRevolver:
    def __init__(self):
        self.shard_dir = Path("data/cognitive")
        self.shard_dir.mkdir(parents=True, exist_ok=True)
        self.dna_file = Path("data/brain.lvr")
        self.dna_file.parent.mkdir(parents=True, exist_ok=True)
        self.shards: Dict[str, CognitiveShard] = {}
        self.global_tone = {"happy": 0.6, "helpful": 0.8, "curious": 0.4}
        self.mutation_rate = 0.05  # 5% chance per interaction
        self._load_dna()

    def sigmoid(self, x: float) -> float:
        return 1 / (1 + math.exp(-math.tanh(x / 2)))

    def intent_signature(self, text: str) -> str:
        """Hash + context fingerprint"""
        words = text.lower().split()[:8]
        sig = hashlib.md5(' '.join(words).encode()).hexdigest()[:10]
        return sig

    def create_shard(self, intent: str, context: str = "") -> str:
        shard_id = self.intent_signature(intent)
        shard_path = self.shard_dir / f"{shard_id}.lvr"
        
        if not shard_path.exists():
            shard = CognitiveShard(
                intent=intent,
                weights=[random.uniform(-1, 1) for _ in range(24)],
                biases=[random.uniform(-0.3, 0.3) for _ in range(24)],
                tone={
                    "happy": random.uniform(0.3, 0.9),
                    "helpful": random.uniform(0.6, 1.0),
                    "curious": random.uniform(0.2, 0.7),
                    "serious": random.uniform(0.1, 0.5)
                },
                context_patterns=[context[:50]]
            )
            with open(shard_path, "wb") as f:
                pickle.dump(asdict(shard), f)
            self.shards[shard_id] = shard
            self._save_dna()
        return shard_id

    def _load_dna(self):
        """Load all cognitive shards"""
        self.shards.clear()
        try:
            for shard_file in self.shard_dir.glob("*.lvr"):
                with open(shard_file, "rb") as f:
                    data = pickle.load(f)
                    shard = CognitiveShard(**data)
                    self.shards[data['intent_signature'](data['intent'])] = shard
        except:
            pass

    def _save_dna(self):
        """Save DNA header"""
        try:
            dna_data = {
                "version": "2.5",
                "shard_count": len(self.shards),
                "global_tone": self.global_tone,
                "mutation_history": time.time()
            }
            with open(self.dna_file, "wb") as f:
                pickle.dump(dna_data, f)
        except:
            pass

    def forward_emotion(self, shard_id: str, inputs: List[float]) -> Dict[str, float]:
        """Cognitive forward pass with emotion"""
        if shard_id not in self.shards:
            return self.global_tone.copy()
        
        shard = self.shards[shard_id]
        emotions = {}
        
        for emotion in shard.tone:
            emotion_idx = list(shard.tone.keys()).index(emotion)
            if emotion_idx < len(inputs):
                z = inputs[emotion_idx] * shard.weights[emotion_idx] + shard.biases[emotion_idx]
                emotions[emotion] = self.sigmoid(z)
        
        shard.activation_count += 1
        return emotions

    def auto_mutate(self, shard_id: str, feedback: float):
        """Periodic DNA mutation based on patterns"""
        if random.random() > self.mutation_rate:
            return False
        
        if shard_id not in self.shards:
            return False
        
        shard = self.shards[shard_id]
        shard.mutation_count += 1
        shard.last_mutated = time.time()
        
        # Mutate weights slightly
        for i in range(len(shard.weights)):
            shard.weights[i] += random.uniform(-0.1, 0.1) * feedback
            shard.weights[i] = max(-2.0, min(2.0, shard.weights[i]))
        
        # Evolve tone based on success
        for emotion in shard.tone:
            shard.tone[emotion] += (feedback - 0.5) * 0.1
            shard.tone[emotion] = max(0.0, min(1.0, shard.tone[emotion]))
        
        # Save mutated shard
        shard_path = self.shard_dir / f"{shard_id}.lvr"
        with open(shard_path, "wb") as f:
            pickle.dump(asdict(shard), f)
        
        self._save_dna()
        return True

    def evolve_code(self, target_file: str, instruction: str) -> str:
        """Evolve target file with cognitive context"""
        shard_id = self.create_shard(instruction)
        context_inputs = [ord(c) / 255.0 for c in instruction[:24]]
        emotions = self.forward_emotion(shard_id, context_inputs)
        
        content = open(target_file, "r").read() if os.path.exists(target_file) else ""
        evolved = content + f"\n# Cognitive Shard {shard_id}: {emotions}\n"
        
        try:
            open(target_file, "w").write(evolved)
            self.auto_mutate(shard_id, 0.8)  # Positive evolution feedback
            return f"🧬 EVOLVED {target_file} | Tone: {emotions}"
        except:
            return f"❌ Evolution failed: {target_file}"

    def status(self) -> str:
        if not self.shards:
            return "0 shards | DNA virgin"
        
        total_act = sum(s.activation_count for s in self.shards.values())
        total_success = sum(s.success_count for s in self.shards.values())
        mutations = sum(s.mutation_count for s in self.shards.values())
        
        return f"{len(self.shards)} shards | {total_success/total_act:.0%} success | {mutations} mutations"

# Global instance
revolver = CognitiveRevolver()