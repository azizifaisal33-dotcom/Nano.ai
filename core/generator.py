"""
💬 NanoGenerator v2 - Response Synthesis Engine
Context-aware response generation with templates
"""
from typing import Dict, List, Optional
import random
from dataclasses import dataclass
import json
from rich.markdown import Markdown
from rich.console import Console

@dataclass
class ResponseTemplate:
    intent: str
    templates: List[str]
    confidence_boost: float = 1.0
    followups: List[str] = None

class NanoGenerator:
    def __init__(self):
        self.console = Console()
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, List[ResponseTemplate]]:
        """Comprehensive response templates"""
        return {
            'system_info': ResponseTemplate(
                intent='system_info',
                templates=[
                    "📊 **System Status**\n```\n{output}\n```",
                    "🔍 Here's your system info:\n{output}",
                    "📈 Monitoring results:\n```\n{output}\n```"
                ],
                confidence_boost=1.2
            ),
            'package_install': ResponseTemplate(
                intent='package_install',
                templates=[
                    "🔧 **Installing {package}**\n```\n{output}\n```\n✅ Done! Ready to use.",
                    "📦 Package {package} installation:\n{output}",
                    "⚙️ Setup complete for {package}"
                ]
            ),
            'network': ResponseTemplate(
                intent='network',
                templates=[
                    "🌐 **Network Status**\n{output}",
                    "📡 Connection details:\n```\n{output}\n```"
                ]
            ),
            'greeting': ResponseTemplate(
                intent='greeting',
                templates=[
                    "👋 Halo! Nano AI v2 siap bantu kamu! 🤖\nApa yang bisa saya lakukan?",
                    "🧠 Hai! Neural brain aktif. Command apa hari ini?",
                    "✨ Selamat datang di Nano AI! 🚀"
                ]
            ),
            'question': ResponseTemplate(
                intent='question',
                templates=[
                    "🤔 {output}\n\nApa lagi yang ingin kamu ketahui?",
                    "💡 Jawaban: {output}",
                    "📚 {output}"
                ]
            ),
            'unknown': ResponseTemplate(
                intent='unknown',
                templates=[
                    "🤖 Belum paham perintah '{input}'\n\nCoba:\n• `cek ram`\n• `install git`\n• `setup web server`",
                    "❓ Perintah baru terdeteksi. Saya akan belajar!\n\nContoh: `cek cpu`, `pkg install python`"
                ]
            )
        }

    def generate(self, intent: str, context: Dict, output: str = "", 
                input_text: str = "") -> str:
        """Generate context-aware response"""
        # Memory recall first
        memory_response = memory.search_similar(input_text)
        if memory_response:
            self.console.print("[blue]💾 Memory recall hit[/]")
            return memory_response[0]['ai_response']
        
        # Template matching
        template = self.templates.get(intent, self.templates['unknown'])
        response = random.choice(template.templates)
        
        # Format with context
        response = response.format(
            output=output,
            package=context.get('entities', {}).get('package', 'package'),
            input=input_text,
            intent=intent
        )
        
        # Learn from this interaction
        memory.add_conversation(
            session_id="default",
            user_input=input_text,
            ai_response=response,
            intent=intent,
            tool_used=context.get('tool', 'generate'),
            success=True
        )
        
        return response

    def stream_response(self, text: str):
        """Typing effect for responses"""
        for char in text:
            yield char
            import time; time.sleep(0.02)

# Global generator
generator = NanoGenerator()