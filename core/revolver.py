import pickle
import os
import random
import hashlib
from pathlib import Path
from typing import List, Dict, Any
import struct

class Revolver:
    def __init__(self, fs, backup):
        self.fs = fs
        self.backup = backup
        self.dna_path = Path("data/brain.lvr")
        self.dna_path.parent.mkdir(exist_ok=True)
        self.dna = self._load_dna()
        print("🔫 Revolver DNA loaded:", len(self.dna) if self.dna else 0)

    def _load_dna(self) -> Dict[str, List[float]]:
        """Load DNA with corruption recovery"""
        if not self.dna_path.exists():
            return {}
        
        try:
            with open(self.dna_path, "rb") as f:
                header = f.read(12)
                if len(header) < 12 or header[:4] != b"NANO":
                    print("⚠️ DNA corrupted - auto repair")
                    return {}
                
                data_size = struct.unpack("Q", header[4:12])[0]
                data = f.read(data_size)
                
                if len(data) != data_size:
                    raise ValueError("Incomplete DNA")
                
                return pickle.loads(data)
        except Exception as e:
            print(f"❌ DNA load failed: {e} - Resetting")
            self.dna_path.unlink(missing_ok=True)
            return {}

    def _save_dna(self):
        """Save DNA with robust binary format"""
        try:
            data = pickle.dumps(self.dna)
            header = b"NANO" + struct.pack("Q", len(data))
            
            with open(self.dna_path, "wb") as f:
                f.write(header + data)
            return True
        except Exception as e:
            print(f"❌ DNA save failed: {e}")
            return False

    def _tokenize_instruction(self, instruction: str) -> List[str]:
        """Convert instruction to DNA tokens"""
        words = instruction.lower().split()
        tokens = []
        for i, word in enumerate(words):
            if i > 0:
                tokens.append(f"{words[i-1]}_{word}")
            tokens.append(word)
        return tokens

    def _instruction_to_dna(self, instruction: str) -> List[float]:
        """Convert instruction to DNA weights"""
        tokens = self._tokenize_instruction(instruction)
        dna_weights = []
        
        for token in tokens:
            h = int(hashlib.md5(token.encode()).hexdigest(), 16)
            weight = (h % 10000) / 10000.0
            dna_weights.append(weight)
        
        return dna_weights

    def evolve(self, target_file: str, instruction: str) -> str:
        """Main evolution method"""
        print(f"🔫 EVOLVING {target_file} with: {instruction[:50]}...")
        
        self.backup.create()
        
        content = self.fs.read(target_file)
        if not content:
            return f"❌ File {target_file} not found"
        
        dna_pattern = self._instruction_to_dna(instruction)
        
        instruction_key = hashlib.md5(instruction.encode()).hexdigest()[:8]
        self.dna[instruction_key] = {
            "file": target_file,
            "instruction": instruction,
            "pattern": dna_pattern,
            "timestamp": os.path.getctime(target_file) if os.path.exists(target_file) else 0
        }
        
        evolved_content = self._apply_evolution(content, instruction, dna_pattern)
        
        if self.fs.write(target_file, evolved_content):
            self._save_dna()
            return f"✅ {target_file} evolved! DNA stored: {instruction_key}"
        else:
            return "❌ Evolution failed - file write error"

    def _apply_evolution(self, content: str, instruction: str, dna_pattern: List[float]) -> str:
        """Apply intelligent code changes based on DNA"""
        lines = content.split('\n')
        evolved_lines = []
        
        intent = self._detect_intent(instruction)
        
        for i, line in enumerate(lines):
            if self._should_modify_line(line, instruction, dna_pattern):
                evolved_line = self._evolve_line(line, intent, dna_pattern)
                evolved_lines.append(f"# 🔫 EVOLVED: {evolved_line}")
            else:
                evolved_lines.append(line)
        
        if "fungsi" in instruction.lower() or "function" in instruction.lower():
            new_func = self._generate_new_function(intent)
            evolved_lines.append(f"\n# 🧬 NEW DNA FUNCTION")
            evolved_lines.extend(new_func.split('\n'))
        
        return '\n'.join(evolved_lines)

    def _detect_intent(self, instruction: str) -> str:
        """Detect evolution intent"""
        text = instruction.lower()
        if any(w in text for w in ["chat", "obrolan", "talk"]):
            return "chat_enhance"
        elif any(w in text for w in ["command", "terminal", "bash"]):
            return "command"
        elif "error" in text or "pengamanan" in text:
            return "safety"
        elif "memory" in text:
            return "memory"
        return "general"

    def _should_modify_line(self, line: str, instruction: str, dna_pattern: List[float]) -> bool:
        """DNA-weighted decision to modify line"""
        line_lower = line.lower()
        instruction_lower = instruction.lower()
        
        score = sum(1 for token in self._tokenize_instruction(instruction) 
                   if token in line_lower)
        return score > 0 and random.random() < 0.7

    def _evolve_line(self, line: str, intent: str, dna_pattern: List[float]) -> str:
        """Evolve single line based on DNA"""
        if intent == "chat_enhance" and 'return' in line:
            return line.replace("return", "return f'{result} 🤖'")
        elif intent == "safety" and 'try:' not in line and 'except' not in line:
            return f"try:\n    {line}"
        return line

    def _generate_new_function(self, intent: str) -> str:
        """Generate new function based on DNA intent - FIXED SYNTAX!"""
        if intent == "chat_enhance":
            return '''def smart_chat(self, text):
    """DNA-enhanced chat with context awareness"""
    if 'nano' in text.lower():
        return '🧠 NanoAI understands you perfectly!'
    return self.chat(text)'''
        
        elif intent == "safety":
            return '''def safe_exec(self, cmd):
    """DNA safety wrapper"""
    if "rm -rf" in cmd.lower() or "sudo" in cmd.lower():
        return '🚫 Dangerous command blocked by DNA'
    import subprocess
    return subprocess.run(cmd, shell=True, capture_output=True).returncode'''
        
        elif intent == "memory":
            return '''def dna_memory(self, key, value):
    """Store in DNA-enhanced memory"""
    self.revolver.dna[key] = value
    self.revolver._save_dna()'''
        
        else:
            return '''def dna_func(self):
    """DNA generated function"""
    pass'''

    def status(self) -> str:
        """DNA status report"""
        total_dna = len(self.dna)
        recent = [v for v in self.dna.values() if 'timestamp' in v]
        return f"DNA Strands: {total_dna} | Recent: {len(recent)}"

    def auto_repair(self):
        """Auto-repair corrupted DNA"""
        old_dna = self.dna
        self.dna = self._load_dna()
        if not self.dna:
            self.dna = {"repair": {"pattern": [0.5]*10}}
            self._save_dna()
            return "🧬 DNA auto-repaired!"
        return "✅ DNA healthy"