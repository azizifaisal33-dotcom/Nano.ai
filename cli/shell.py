import sys
from core.brain import Brain


class NanoShell:
    def __init__(self):
        self.brain = Brain()
        self.running = True

    def start(self):
        print("🧠 Nano AI Shell (V25)")
        print("Ketik 'exit' untuk keluar\n")

        while self.running:
            try:
                user_input = input("➜ ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit"]:
                    self.running = False
                    break

                result = self.brain.think(user_input)

                print(result)

            except KeyboardInterrupt:
                print("\n⛔ dihentikan")
                break

            except Exception as e:
                print(f"❌ error: {e}")


def main():
    shell = NanoShell()
    shell.start()


if __name__ == "__main__":
    main()