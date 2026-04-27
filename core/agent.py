import time

class Agent:
    def __init__(self, brain):
        self.brain = brain
        self.running = False
        self.goal = None

    def start(self, goal):
        if self.running:
            return "agent sudah jalan"

        self.running = True
        self.goal = goal

        steps = 0
        while self.running and steps < 20:
            steps += 1

            result = self.brain.think(goal)

            if "berhasil" in str(result).lower():
                self.running = False
                return f"🎯 selesai di step {steps}"

            time.sleep(1)

        self.running = False
        return "⚠️ agent berhenti"

    def stop(self):
        self.running = False
        return "agent dihentikan"