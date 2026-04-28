import pickle
import os
import random
import hashlib
from pathlib import Path
from typing import List, Dict
import struct

class Revolver:
    def __init__(self, fs, backup):
        self.fs = fs
        self.backup = backup
        self.dna_path = Path("data/brain.lvr")
        self.dna_path.parent.mkdir(exist_ok=True)
        
        # ✅ FORCE CLEAN DNA CORRUPTION ON START
        if self.dna_path.exists():
            try:
                self.dna_path.unlink()
                print("🧬 Corrupted DNA deleted")
            except:
                pass
        
        self.dna = {}
        print("🔫 Revolver: Fresh DNA initialized ✓")

    def _load_dna(self) -> Dict:
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
            print(f"❌ DNA load failed: {e}")
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
        return "❌ Evolution failed"

    def _apply_evolution(self, content: str, instruction: str, dna_pattern: List[float]) -> str:
        lines = content.split('\n')
        evolved_lines = []
        intent = self._detect_intent(instruction)
        
        for line in lines:
            if self._should_modify_line(line, instruction, dna_pattern):
                evolved_line = self._evolve_line(line, intent)
                evolved_lines.append(f"# 🔫 EVOLVED: {evolved_line}")
            else:
                evolved_lines.append(line)
        
        if "fungsi" in instruction.lower() or "function" in instruction.lower():
            new_func = self._generate_new_function(intent)
            evolved_lines.extend(["", "# 🧬 NEW DNA FUNCTION"] + new_func.split('\n'))
        
        return '\n'.join(evolved_lines)

    def _detect_intent(self, instruction: str) -> str:
        text = instruction.lower()
        if any(w in text for w in ["chat", "obrolan"]): return "chat_enhance"
        if any(w in text for w in ["command", "terminal"]): return "command"
        if "error" in text or "pengamanan" in text: return "safety"
        if "memory" in text: return "memory"
        return "general"

    def _should_modify_line(self, line: str, instruction: str, dna_pattern: List[float]) -> bool:
        line_lower = line.lower()
        score = sum(1 for token in self._tokenize_instruction(instruction) if token in line_lower)
        return score > 0 and random.random() < 0.6

    def _evolve_line(self, line: str, intent: str) -> str:
        if intent == "chat_enhance" and 'return' in line:
            return line.replace("return", "return f'{result} 😎'")
        return line

    def _generate_new_function(self, intent: str) -> str:
        funcs = {
            "chat_enhance": '''def smart_chat(self, text):
    if 'halo' in text.lower():
        return 'Yo bro! 👊 Siap bantu!'
    return self.chat(text)''',
            "safety": '''def safe_exec(self, cmd):
    if any(d in cmd.lower() for d in ["rm -rf", "sudo"]):
        return "🚫 Blocked by DNA!"
    return cmd''',
            "memory": '''def dna_save(self, key, data):
    self.revolver.dna[key] = data
    self.revolver._save_dna()'''
        }
        return funcs.get(intent, "def dna_func(self): pass")

    def status(self) -> str:
        return f"DNA Strands: {len(self.dna)}"

    def auto_repair(self):
        self.dna = {"repair": [0.5]*10}
        self._save_dna()
        return "🧬 DNA repaired!"