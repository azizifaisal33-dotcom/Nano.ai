
#!/usr/bin/env python3
import os
import pickle
import struct
import hashlib
import time
import random
import math
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class Shard:
    intent: str
    weights: List[float]
    biases: List[float]
    activation_count: int = 0
    success_count: int = 0
    last_updated: float = 0.0
    version: str = "2.5"

class NeuralSharding:
    def __init__(self):
        self.shard_dir = Path("data/shards")
        self.shard_dir.mkdir(parents=True, exist_ok=True)
        self.header_file = Path("data/brain.lvr")
        self.backup_file = Path("data/brain_backup.lvr")
        self.shards: Dict[str, Shard] = {}
        self.global_weights = [0.5] * 32  # 32 neurons
        self.global_biases = [0.0] * 32
        self.learning_rate = 0.02
        self._init_header()
        self.load_all_shards()

    def _init_header(self):
        """Auto-repair corrupt header"""
        try:
            if self.header_file.exists():
                with open(self.header_file, "rb") as f:
                    header = f.read(8)
                    if len(header) != 8 or header[:4] != b"NANO":
                        raise ValueError("Corrupt header")
            else:
                # Create fresh header
                header_data = {
                    "version": "2.5",
                    "global_weights": self.global_weights,
                    "global_biases": self.global_biases,
                    "shard_count": 0,
                    "timestamp": time.time()
                }
                with open(self.header_file, "wb") as f:
                    pickle.dump(header_data, f)
                self._backup()
                print("🧬 brain.lvr header initialized")
        except:
            self._recover_from_backup()

    def _recover_from_backup(self):
        """Auto-restore from backup"""
        try:
            if self.backup_file.exists():
                self.header_file.write_bytes(self.backup_file.read_bytes())
                print("🧬 Recovered from backup")
            else:
                self._init_header()
        except:
            self._init_header()

    def _backup(self):
        """Atomic backup"""
        try:
            self.header_file.replace(self.backup_file)
        except:
            pass

    def sigmoid(self, x: float) -> float:
        if x > 10: return 1.0
        if x < -10: return 0.0
        return 1 / (1 + math.exp(-x))

    def sigmoid_deriv(self, x: float) -> float:
        s = self.sigmoid(x)
        return s * (1 - s)

    def intent_hash(self, intent: str) -> str:
        return hashlib.md5(intent.lower().encode()).hexdigest()[:8]

    def get_shard_path(self, shard_id: str) -> Path:
        return self.shard_dir / f"{shard_id}.lvr"

    def create_shard(self, intent: str) -> str:
        shard_id = self.intent_hash(intent)
        shard_path = self.get_shard_path(shard_id)
        
        if not shard_path.exists():
            shard = Shard(
                intent=intent,
                weights=[random.uniform(-1, 1) for _ in range(32)],
                biases=[random.uniform(-0.5, 0.5) for _ in range(32)]
            )
            try:
                with open(shard_path, "wb") as f:
                    pickle.dump(asdict(shard), f)
                self.shards[shard_id] = shard
                self._update_header(shard_id)
                print(f"🧬 Shard created: {shard_id}")
            except:
                pass
        return shard_id

    def load_all_shards(self):
        """Load all shards"""
        self.shards.clear()
        try:
            for shard_file in self.shard_dir.glob("*.lvr"):
                try:
                    with open(shard_file, "rb") as f:
                        data = pickle.load(f)
                        shard = Shard(**data)
                        self.shards[shard.intent_hash(shard.intent)] = shard
                except:
                    shard_file.unlink()  # Delete corrupt shard
        except:
            pass

    def _update_header(self, shard_id: str = None):
        """Update header shard count"""
        try:
            header_data = {
                "version": "2.5",
                "global_weights": self.global_weights,
                "global_biases": self.global_biases,
                "shard_count": len(self.shards),
                "timestamp": time.time()
            }
            with open(self.header_file, "wb") as f:
                pickle.dump(header_data, f)
            self._backup()
        except:
            pass

    def forward(self, shard_id: str, inputs: List[float]) -> List[float]:
        """Neural forward pass"""
        if shard_id not in self.shards:
            return [0.5] * 32
            
        shard = self.shards[shard_id]
        outputs = []
        
        for i in range(32):
            inp = inputs[i] if i < len(inputs) else 0.0
            z = inp * shard.weights[i] + shard.biases[i]
            outputs.append(self.sigmoid(z))
        
        shard.activation_count += 1
        return outputs

    def mini_backprop(self, shard_id: str, inputs: List[float], target: float, feedback: bool):
        """Pure Python backpropagation"""
        if shard_id not in self.shards:
            return
            
        shard = self.shards[shard_id]
        prediction = max(self.forward(shard_id, inputs))
        error = target - prediction
        delta = error * self.sigmoid_deriv(prediction)
        
        # Update weights & biases
        for i in range(32):
            inp = inputs[i] if i < len(inputs) else 0.0
            shard.weights[i] += self.learning_rate * delta * inp
            shard.biases[i] += self.learning_rate * delta
        
        # Update success metrics
        if feedback:
            shard.success_count += 1
        shard.last_updated = time.time()
        
        # Save shard
        shard_path = self.get_shard_path(shard_id)
        try:
            with open(shard_path, "wb") as f:
                pickle.dump(asdict(shard), f)
        except:
            pass

    def analyze(self, intent: str) -> Dict[str, Any]:
        """Get neural recommendation"""
        shard_id = self.create_shard(intent)
        inputs = [ord(c) % 256 / 255.0 for c in intent[:32]]
        outputs = self.forward(shard_id, inputs)
        
        confidence = max(outputs)
        action = "EVOLVE" if confidence > 0.8 else "ADAPT" if confidence > 0.5 else "STABLE"
        
        shard = self.shards.get(shard_id, Shard(intent="", weights=[], biases=[]))
        success_rate = shard.success_count / max(1, shard.activation_count)
        
        return {
            "shard_id": shard_id,
            "confidence": confidence,
            "action": action,
            "success_rate": success_rate,
            "recommendation": f"{action} weights for '{intent}'"
        }

class Revolver:
    def __init__(self, fs, backup):
        self.fs = fs
        self.backup = backup
        self.neural = NeuralSharding()

    def status(self) -> str:
        total_shards = len(self.neural.shards)
        avg_success = sum(s.success_count / max(1, s.activation_count) 
                         for s in self.neural.shards.values())
        avg_success = avg_success / max(1, total_shards)
        return f"{total_shards} shards | {avg_success:.1%} success | LR:{self.neural.learning_rate:.3f}"

    def evolve(self, target_file: str, instruction: str) -> str:
        try:
            # Neural analysis
            analysis = self.neural.analyze(instruction)
            print(f"🧠 [{analysis['shard_id']}] {analysis['confidence']:.2f} {analysis['action']}")
            
            # Read target
            content = self.fs.read(target_file)
            if not content:
                return f"❌ {target_file} not found"
            
            # Generate evolution
            new_content = self._evolve_content(content, instruction, analysis)
            
            # Apply with backup
            if self.backup.create() and self.fs.write(target_file, new_content):
                # Positive feedback
                inputs = [ord(c) % 256 / 255.0 for c in instruction[:32]]
                self.neural.mini_backprop(analysis['shard_id'], inputs, 1.0, True)
                return f"✅ EVOLVED {target_file} | {analysis['shard_id']}"
            else:
                inputs = [ord(c) % 256 / 255.0 for c in instruction[:32]]
                self.neural.mini_backprop(analysis['shard_id'], inputs, 0.0, False)
                return "❌ Evolution failed - DNA protected"
        except Exception as e:
            return f"💥 {e}"

    def _evolve_content(self, content: str, instruction: str, analysis: Dict) -> str:
        """Intelligent code transformation"""
        lines = content.splitlines()
        evolved = []
        
        for line in lines:
            if 'def think' in line or 'def evolve' in line:
                evolved.append(f"        # Neural {analysis['shard_id']}: {analysis['action']}")
            evolved.append(line)
        
        # Add neural footer
        footer = f"""
# Neural Shard: {analysis['shard_id']} | Success: {analysis['success_rate']:.1%}
# Auto-evolved: {time.ctime()}
"""
        return '\n'.join(evolved) + footer

    def feedback(self, shard_id: str, success: bool):
        """Agent feedback loop"""
        inputs = [random.random() for _ in range(32)]
        self.neural.mini_backprop(shard_id, inputs, 1.0 if success else 0.0, success)