import os
import time
from core.brain import Brain


class Dashboard:
    def __init__(self):
        self.brain = Brain()

    def clear(self):
        os.system("clear")

    def show(self):
        while True:
            try:
                self.clear()

                print("🧠 NANO AI DASHBOARD")
                print("=" * 40)

                # =====================
                # BASIC INFO
                # =====================
                print("Status       : RUNNING")
                print(f"Agent Active : {self.brain.agent.running}")
                print(f"Goal         : {self.brain.agent.goal}")

                # =====================
                # AGENT LOG
                # =====================
                print("\n📊 Agent Log:")
                logs = self.brain.agent.history[-5:]

                if not logs:
                    print("- belum ada aktivitas")
                else:
                    for l in logs:
                        print(f"{l['step']}: {l['result']}")

                # =====================
                # MENU
                # =====================
                print("\n[1] Start Agent")
                print("[2] Stop Agent")
                print("[3] Refresh")
                print("[4] Exit")

                choice = input("\nPilih: ").strip()

                if choice == "1":
                    goal = input("Masukkan goal: ")
                    print(self.brain.agent.start(goal))
                    input("Enter...")

                elif choice == "2":
                    print(self.brain.agent.stop())
                    input("Enter...")

                elif choice == "3":
                    continue

                elif choice == "4":
                    break

            except KeyboardInterrupt:
                break


def main():
    dash = Dashboard()
    dash.show()


if __name__ == "__main__":
    main()