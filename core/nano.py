"""
🧠 NanoAI v2 - Master Neural Brain (Clean & Lightweight)
No NumPy, No Rich - Pure Terminal Colors - 100% Stable
"""

import random
from typing import Dict, List, Any, Optional
from core.tokenizer import tokenizer
from core.vector import vectorstore
from core.intent import intent_engine
# from core.memory import memory  <-- Hapus jika folder memory sudah kamu delete
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
        
    def think(self, user_input: str) -> Dict[str, Any]:
        """Complete neural thinking pipeline"""
        print(f"\n{Color.BOLD}{Color.CYAN}🧠 NanoAI thinking...{Color.END}")
        
        # 1. TOKENIZATION
        token_ids = tokenizer.encode(user_input)
        print(f"📝 Tokens: {len(token_ids)}")
        
        # 2. INTENT DETECTION
        intents = intent_engine.detect(user_input)
        # Ambil intent pertama jika ada
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
        
        if top_intent and intent_name in ['system_info', 'package_install']:
            tool_used = intent_name
            cmd = self._build_command(top_intent, user_input)
            execution_result = self.engine.run(cmd)
        
        # 5. RESPONSE GENERATION
        response = generator.generate(
            intent=intent_name,
            context={
                'entities': top_intent.entities if top_intent else {},
                'tool': tool_used,
                'memory_hit': memory_hit
            },
            output=execution_result['output'],
            input_text=user_input
        )
        
        # 6. LEARN & EVOLVE (Revolver DNA Update)
        revolver.evolve(user_input.split())
        
        # 7. VECTOR STORE UPDATE (Optional)
        vectorstore.add(user_input, query_embedding, {
            'intent': intent_name,
            'session': self.session_id
        })
        
        return {
            'input': user_input,
            'tokens': len(token_ids),
            'top_intent': intent_name,
            'tool_used': tool_used,
            'memory_hit': memory_hit,
            'response': response,
            'success': execution_result['success']
        }

    def _dummy_embedding(self, token_ids: List[int]) -> List[float]:
        seed = sum(token_ids) % 1000
        random.seed(seed)
        return [random.uniform(-1, 1) for _ in range(384)]

    def _build_command(self, intent_match: Any, input_text: str) -> str:
        if intent_match.name == 'package_install':
            pkg = intent_match.entities.get('arg1', 'python')
            return f"pkg install {pkg} -y"
        elif intent_match.name == 'system_info':
            return "free -h && df -h && uptime"
        return "echo 'Command executed'"

    def show_thinking(self, result: Dict):
        """Manual Panel Visualization"""
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

# Global instance
nano_ai = NanoAI()
