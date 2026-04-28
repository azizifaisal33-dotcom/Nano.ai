import random
from collections import defaultdict

class CharModel:
    def __init__(self):
        self.chain = defaultdict(list)

    # =========================
    # TRAINING
    # =========================
    def train(self, text):
        text = text.lower()

        for i in range(len(text) - 1):
            current = text[i]
            next_char = text[i + 1]

            if current.isalpha():
                self.chain[current].append(next_char)

    # =========================
    # GENERATE TEXT
    # =========================
    def generate(self, start="h", length=10):
        result = start

        current = start

        for _ in range(length):
            if current not in self.chain:
                current = random.choice(list(self.chain.keys()))

            next_chars = self.chain[current]

            if not next_chars:
                break

            current = random.choice(next_chars)
            result += current

        return result