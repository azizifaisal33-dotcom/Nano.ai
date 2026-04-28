from core.brain import Brain

if __name__ == "__main__":
    brain = Brain()

    print("\n💬 Nano AI ACTIVE\n")

    while True:
        try:
            user = input("you> ").strip()

            if user.lower() in ["exit", "quit"]:
                print("bye")
                break

            print("\n🧠 AI:\n", brain.think(user), "\n")

        except KeyboardInterrupt:
            print("\nbye")
            break

        except Exception as e:
            print("⚠️ error:", e)