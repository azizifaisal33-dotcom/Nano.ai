
import random

class SimpleGenerator:
    def __init__(self):
        self.chain = {}

    def train(self, text):
        words = text.lower().split()

        for i in range(len(words) - 1):
            a, b = words[i], words[i + 1]

            if a not in self.chain:
                self.chain[a] = []

            self.chain[a].append(b)

    def generate(self, start="halo", length=8):
        current = start
        result = [current]

        for _ in range(length):
            if current not in self.chain:
                break

            current = random.choice(self.chain[current])
            result.append(current)

        return " ".join(result)