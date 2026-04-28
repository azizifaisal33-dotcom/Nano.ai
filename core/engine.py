from core.command_ai import CommandAI
from core.generator import NanoGenerator  # Direct import, not 'generator'

class NanoEngine:
    def __init__(self):
        self.cmd_ai = CommandAI()
        self.generator = NanoGenerator()
        print("⚙️ NanoEngine: Murni Aktif")

    def generate(self, user_input):
        commands = self.cmd_ai.generate(user_input)
        if commands and commands[0] != user_input:
            return f"Saran perintah: {', '.join(commands[:3])}"
        return self.generator.reply(user_input)

engine = NanoEngine()