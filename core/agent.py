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

        self.running = True
        self.goal = goal
        self.history = []

        steps = 0

        while self.running and steps < 20:
            steps += 1

            # AI berpikir berdasarkan goal
            result = self.brain.think(goal)

            # simpan log
            self.history.append({
                "step": steps,
                "goal": goal,
                "result": result
            })

            # cek selesai
            if isinstance(result, str):
                low = result.lower()
                if "berhasil" in low or "success" in low or "selesai" in low:
                    self.running = False
                    return f"🎯 goal selesai di step {steps}"

            time.sleep(1)

        self.running = False
        return "⚠️ agent berhenti (limit)"

    def stop(self):
        self.running = False
        return "agent dihentikan"

    def log(self):
        if not self.history:
            return "tidak ada log"
        return "\n".join([f"{h['step']}: {h['result']}" for h in self.history[-10:]])