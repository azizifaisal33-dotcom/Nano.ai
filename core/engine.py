"""
⚙️ NanoEngine - 100% Buatan Sendiri
Menggunakan logika internal tanpa library eksternal.
"""
from core.generator import generator
from core.command_ai import CommandAI

class NanoEngine:
    def __init__(self):
        self.cmd_ai = CommandAI()
        print("⚙️ NanoEngine: Murni Aktif (Bebas dari karya orang lain)")

    def generate(self, user_input):
        # 1. Cek apakah ini perintah terminal (lewat CommandAI kamu)
        commands = self.cmd_ai.generate(user_input)
        
        # 2. Jika bukan perintah sistem, gunakan Generator Markov milikmu
        if not commands or commands == user_input:
            return generator.reply(user_input)
            
        return f"Saran perintah: {', '.join(commands)}"

engine = NanoEngine()
