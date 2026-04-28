"""
🧠 NanoAI v2 - Master Neural Brain (Clean Version)
Full AI orchestration pipeline without NumPy
"""

import random
from typing import Dict, List, Any, Optional
from core.tokenizer import tokenizer
from core.vector import vectorstore
from core.intent import intent_engine
from core.memory import memory
from core.generator import generator
from core.engine import NanoEngine
from core.math_utils import NanoMath # Menggunakan utilitas buatan sendiri
from core.revolver import revolver    # Integrasi mesin evolusi
from rich.console import Console
from rich.panel import Panel

class NanoAI:
    def __init__(self):
        self.console = Console()
        self.engine = NanoEngine()
        self.session_id = "nano-session-001"
        
    def think(self, user_input: str) -> Dict[str, Any]:
        """Complete neural thinking pipeline"""
        self.console.print(f"\n[bold cyan]🧠 NanoAI thinking...[/]")
        
        # 1. TOKENIZATION
        token_ids = tokenizer.encode(user_input)
        self.console.print(f"📝 Tokens: {len(token_ids)}")
        
        # 2. INTENT DETECTION
        intents = intent_engine.detect(user_input)
        top_intent = intents if intents else None
        self.console.print(f"🎯 Top intent: {top_intent.name if top_intent else 'unknown'}")
        
        # 3. VECTOR MEMORY SEARCH (Pure Python Embedding)
        query_embedding = self._dummy_embedding(token_ids)
        similar = vectorstore.search(query_embedding, k=3)
        memory_hit = bool(similar)
        
        # 4. EXECUTION / TOOL CALL
        tool_used = "generate"
        execution_result = {"output": "", "success": True}
        
        if top_intent and top_intent.name in ['system_info', 'package_install']:
            tool_used = top_intent.name
            cmd = self._build_command(top_intent, user_input)
            execution_result = self.engine.run(cmd)
        
        # 5. RESPONSE GENERATION
        response = generator.generate(
            intent=top_intent.name if top_intent else 'unknown',
            context={
                'entities': top_intent.entities if top_intent else {},
                'tool': tool_used,
                'memory_hit': memory_hit
            },
            output=execution_result['output'],
            input_text=user_input
        )
        
        # 6. LEARN & EVOLVE (Revolver Integration)
        # Sekarang NanoAI otomatis melatih Revolver setiap kali ada input
        revolver.evolve(user_input.split())
        
        # 7. MEMORY UPDATE
        memory.add_conversation(
            session_id=self.session_id,
            user_input=user_input,
            ai_response=response,
            intent=top_intent.name if top_intent else 'unknown',
            tool_used=tool_used,
            success=execution_result['success']
        )
        
        # 8. VECTOR STORE UPDATE
        vectorstore.add(user_input, query_embedding, {
            'intent': top_intent.name if top_intent else 'unknown',
            'session': self.session_id
        })
        
        return {
            'input': user_input,
            'tokens': len(token_ids),
            'intents': [m.name for m in intents],
            'top_intent': top_intent.name if top_intent else 'unknown',
            'tool_used': tool_used,
            'memory_hit': memory_hit,
            'similar_docs': len(similar),
            'response': response,
            'success': execution_result['success']
        }

    def _dummy_embedding(self, token_ids: List[int]) -> List[float]:
        """Placeholder embedding - Menggunakan Python murni (Tanpa NumPy)"""
        # Gunakan sum dari token sebagai seed agar hasilnya konsisten untuk input yang sama
        seed = sum(token_ids) % 1000
        random.seed(seed)
        
        # Membuat vektor 384 dimensi (standar model AI ringan)
        embedding = [random.uniform(-1, 1) for _ in range(384)]
        return embedding

    def _build_command(self, intent_match: Any, input_text: str) -> str:
        """Dynamic command construction"""
        if intent_match.name == 'package_install':
            pkg = intent_match.entities.get('arg1', 'python')
            return f"pkg install {pkg} -y"
        elif intent_match.name == 'system_info':
            if 'ram' in input_text.lower():
                return "free -h"
            return "free -h && df -h && uptime"
        return "echo 'Command executed'"

    def show_thinking(self, result: Dict):
        """Rich thinking visualization"""
        panel = Panel.fit(
            f"""
**Input**: {result['input'][:50]}...
**Intent**: {result['top_intent']} 
**Tool**: {result['tool_used']}
**Memory**: {'✅ Hit' if result['memory_hit'] else '❌ Miss'}
**Success**: {'✅' if result['success'] else '❌'}
            """,
            title="🧠 NanoAI Thinking",
            border_style="blue"
        )
        self.console.print(panel)

# Global instance
nano_ai = NanoAI()
