import random
from collections import defaultdict

class CharAI:
    def __init__(self):
        self.chain = defaultdict(list)

    def train(self, text):
        text = text.lower()

        for i in range(len(text) - 1):
            a = text[i]
            b = text[i + 1]

            if a.isalpha():
                self.chain[a].append(b)

    def generate(self, start="h", length=10):
        result = start
        current = start

        for _ in range(length):
            if current not in self.chain:
                break

            next_chars = self.chain[current]
            if not next_chars:
                break

            current = random.choice(next_chars)
            result += current

        return result