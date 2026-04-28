from core.brain import Brain


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    brain = Brain()

    print("\n💬 Nano AI ACTIVE\n")

    while True:
        try:
            user = input("you> ").strip()

            # =========================
            # EXIT COMMAND
            # =========================
            if user.lower() in ["exit", "quit"]:
                print("bye")
                break

            # =========================
            # PROCESS INPUT
            # =========================
            response = brain.think(user)

            print("\n🧠 AI:\n", response, "\n")

        # =========================
        # SAFE EXIT
        # =========================
        except KeyboardInterrupt:
            print("\nbye")
            break

        # =========================
        # ERROR HANDLER
        # =========================
        except Exception as e:
            print("⚠️ error:", e)