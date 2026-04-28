import sys
import os
from core.brain import Brain

class NanoShell:
    def __init__(self, brain=None):  # ✅ FIXED: Accept brain param
        if brain is None:
            self.brain = Brain()
        else:
            self.brain = brain
        self.running = True

    def start(self):
        os.system('clear' if os.name=='posix' else 'cls')
        print("🧠 Nano AI Shell (V2.5) - DNA Evolution Active")
        print("Commands: evolve, agent, status, help | 'exit' to quit")
        print("=" * 60)

        while self.running:
            try:
                user_input = input("\n➜ ").strip()
                if not user_input: 
                    continue

                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("👋 DNA preserved. Goodbye!")
                    break

                if user_input.lower() == "help":
                    self.show_help()
                    continue

                result = self.brain.think(user_input)
                print(result)

            except KeyboardInterrupt:
                print("\n⛔ Interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def show_help(self):
        print("""
🔫 DNA EVOLUTION COMMANDS:
  evolve core/brain.py "jawab santai dan fun"
  evolve core/nano.py "tambah fitur baru"

🤖 AGENT MODE:
  agent buat file test.py dengan hello world

📊 SYSTEM:
  status    - Brain + DNA status
  help      - This help
  exit      - Shutdown
        """)

if __name__ == "__main__":
    shell = NanoShell()
    shell.start()