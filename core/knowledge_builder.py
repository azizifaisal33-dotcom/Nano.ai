import os
import hashlib

KB_PATH = "data/knowledge/base.txt"


# =========================
# SIMPAN KNOWLEDGE BARU
# =========================
def add_knowledge(question, answer):
    os.makedirs("data/knowledge", exist_ok=True)

    line = f"{question.lower()}|{answer}\n"

    # hindari duplikat sederhana
    key = hashlib.md5(line.encode()).hexdigest()

    if os.path.exists(KB_PATH):
        with open(KB_PATH, "r") as f:
            if line.strip() in f.read():
                return False

    with open(KB_PATH, "a") as f:
        f.write(line)

    return True