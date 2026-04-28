from core.brain import Brain


def main():
    brain = Brain()

    print("\n💬 Nano AI ACTIVE\n")

    while True:
        try:
            user = input("you> ").strip()

            if user.lower() in ["exit", "quit"]:
                print("bye")
                break

            result = brain.think(user)
            print("\n🧠 AI:\n", result, "\n")

        except KeyboardInterrupt:
            print("\nbye")
            break

        except Exception as e:
            print("⚠️ system error:", e)


if __name__ == "__main__":
    main()