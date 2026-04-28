import sys
import os
from core.brain import Brain

class NanoShell:
    def __init__(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        self.brain = Brain()
        self.running = True
        self.history = []

    def start(self):
        print("🧠 Nano AI Shell (V25) - Type 'help' for commands")
        print("=" * 50)
        
        while self.running:
            try:
                user_input = input("\n➜ ").strip()
                if not user_input: continue

                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("👋 Sampai jumpa!")
                    break

                if user_input.lower() == "help":
                    self.show_help()
                    continue

                if user_input.lower() == "status":
                    print(self.brain.status())
                    continue

                result = self.brain.think(user_input)
                print(result)
                self.history.append(f"Q: {user_input}\nA: {result}\n")

            except KeyboardInterrupt:
                print("\n\n⛔ Dihentikan oleh user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def show_help(self):
        help_text = """
📋 COMMANDS:
  agent <goal>     - Start AI agent
  evolve <file> <inst> - Evolve code file
  status           - Show brain status
  help             - Show this help
  exit/quit        - Exit shell
        """
        print(help_text)

if __name__ == "__main__":
    shell = NanoShell()
    shell.start()