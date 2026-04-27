import time

class Agent:
    def __init__(self, brain):
        self.brain = brain
        self.running = False
        self.goal = None
        self.history = []

    def start(self, goal):
        if self.running:
            return "agent sudah jalan"

        self.goal = goal
        self.running = True

        return self.loop()

    def stop(self):
        self.running = False
        return "agent dihentikan"

    def loop(self):
        steps = 0

        while self.running and steps < 20:
            steps += 1

            # THINK
            plan = f"cara mencapai: {self.goal}"
            result = self.brain.think(plan)

            # SIMPAN
            self.history.append({
                "step": steps,
                "plan": plan,
                "result": result
            })

            # CHECK selesai
            if "success" in result.lower() or "selesai" in result.lower():
                self.running = False
                return f"🎯 goal selesai di step {steps}"

            time.sleep(2)

        self.running = False
        return "⚠️ agent berhenti (limit)"