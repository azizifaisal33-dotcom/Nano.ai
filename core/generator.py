import random
import re
from collections import defaultdict


class NanoGenerator:
    """
    Simple learning word-chain generator (Markov style ringan)
    cocok untuk Nano AI Brain
    """

    def __init__(self):
        # kata -> kemungkinan kata berikutnya
        self.chain = defaultdict(list)

        # kata awal untuk starting point random
        self.start_words = []

    # =========================
    # CLEAN TEXT
    # =========================
    def _clean(self, text):
        text = text.lower().strip()
        text = re.sub(r"\s+", " ", text)
        return text

    # =========================
    # TRAIN / BELAJAR
    # =========================
    def train(self, text):
        text = self._clean(text)
        words = text.split()

        if len(words) < 2:
            return

        # simpan kata awal
        self.start_words.append(words[0])

        for i in range(len(words) - 1):
            a, b = words[i], words[i + 1]
            self.chain[a].append(b)

    # =========================
    # GENERATE TEKS
    # =========================
    def generate(self, start=None, length=10):
        if not self.chain:
            return "aku belum punya cukup data untuk belajar"

        # kalau tidak ada start
        if not start:
            start = random.choice(self.start_words) if self.start_words else random.choice(list(self.chain.keys()))

        current = start
        result = [current]

        for _ in range(length):
            if current not in self.chain or not self.chain[current]:
                break

            current = random.choice(self.chain[current])
            result.append(current)

        return " ".join(result)

    # =========================
    # RESPONSE ENGINE (UNTUK BRAIN)
    # =========================
    def reply(self, text):
        text = self._clean(text)
        words = text.split()

        start = words[0] if words else None

        return self.generate(start=start, length=12)