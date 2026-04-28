import random
import re
from typing import List, Dict, Any, Optional

from core.tokenizer import tokenizer
from core.vector import vectorstore
from core.intent import intent_engine
from core.generator import generator
from core.engine import NanoEngine
from core.math_utils import NanoMath 
from core.revolver import revolver    

# =========================
# MANUAL COLORS (ANSI)
# =========================
class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

class NanoAI:
    def __init__(self):
        self.engine = NanoEngine()
        self.session_id = "nano-session-001"
        # Memastikan folder data ada untuk penyimpanan biner/sqlite
        import os
        os.makedirs("data", exist_ok=True)

    def start_shell(self):
        """Koneksi ke CLI Shell (Fix AttributeError)"""
        from cli.shell import NanoShell
        shell = NanoShell()
        shell.start()

    def think(self, user_input: str) -> Dict[str, Any]:
        """Full neural thinking pipeline - 100% Custom"""
        print(f"\n{Color.BOLD}{Color.CYAN}🧠 NanoAI thinking...{Color.END}")

        # 1. TOKENIZATION
        token_ids = tokenizer.encode(user_input)
        print(f"📝 Tokens: {len(token_ids)}")

        # 2. INTENT DETECTION
        intents = intent_engine.detect(user_input)
        # Ambil intent teratas jika ada
        top_intent = intents if (isinstance(intents, list) and len(intents) > 0) else None
        
        intent_name = top_intent.name if top_intent else 'unknown'
        print(f"🎯 Top intent: {Color.YELLOW}{intent_name}{Color.END}")

        # 3. VECTOR MEMORY SEARCH
        query_embedding = self._dummy_embedding(token_ids)
        similar = vectorstore.search(query_embedding, k=3)
        memory_hit = bool(similar)

        # 4. EXECUTION / TOOL CALL
        tool_used = "generate"
        execution_result = {"output": "", "success": True}

        if top_intent and intent_name in ['system_info', 'package_install', 'file_ops']:
            tool_used = intent_name
            cmd = self._build_command(top_intent, user_input)
            execution_result = self.engine.run(cmd)

        # 5. RESPONSE GENERATION
        # Menggunakan generator internal (Markov/Custom)
        response = generator.generate(
            start=user_input.split() if user_input.split() else None,
            length=15
        )

        # 6. LEARN & EVOLVE (Revolver DNA Update)
        # Update file .lvr secara biner
        revolver.evolve(user_input.split())

        # 7. VECTOR STORE UPDATE
        vectorstore.add(user_input, query_embedding, {
            'intent': intent_name,
            'session': self.session_id
        })

        # Kembalikan hasil untuk ditampilkan di shell
        result = {
            'input': user_input,
            'tokens': len(token_ids),
            'top_intent': intent_name,
            'tool_used': tool_used,
            'memory_hit': memory_hit,
            'response': response,
            'success': execution_result['success']
        }
        
        # Tampilkan panel berpikir secara visual
        self.show_thinking(result)
        
        return result

    def _dummy_embedding(self, token_ids: List[int]) -> List[float]:
        """Pembangkit vector sederhana tanpa library external"""
        seed = sum(token_ids) % 1000
        random.seed(seed)
        # Output 384 dimensi sesuai standar NanoVectorStore
        return [random.uniform(-1, 1) for _ in range(384)]

    def _build_command(self, intent_match: Any, input_text: str) -> str:
        """Translasi intent menjadi perintah bash Termux"""
        name = getattr(intent_match, 'name', 'unknown')
        entities = getattr(intent_match, 'entities', {})

        if name == 'package_install':
            pkg = entities.get('arg1', 'python')
            return f"pkg install {pkg} -y"
        elif name == 'system_info':
            return "free -h && df -h && uptime"
        elif name == 'file_ops':
            return "ls -la"
        return "echo 'Command processed'"

    def show_thinking(self, result: Dict):
        """Visualisasi proses berpikir (Manual pengganti Rich)"""
        line = "─" * 40
        m_status = f"{Color.GREEN}✅ Hit{Color.END}" if result['memory_hit'] else f"{Color.RED}❌ Miss{Color.END}"
        s_status = f"{Color.GREEN}✅{Color.END}" if result['success'] else f"{Color.RED}❌{Color.END}"

        print(f"{Color.CYAN}┌{line}┐")
        print(f"│ {Color.BOLD}🧠 NanoAI Thinking Details{Color.END}")
        print(f"├{line}┤")
        print(f"│ Input  : {result['input'][:30]}...")
        print(f"│ Intent : {result['top_intent']}")
        print(f"│ Tool   : {result['tool_used']}")
        print(f"│ Memory : {m_status}")
        print(f"│ Success: {s_status}")
        print(f"{Color.CYAN}└{line}┘{Color.END}")
        print(f"\n{Color.BOLD}Assistant:{Color.END} {result['response']}")

# Global instance
nano_ai = NanoAI()
