import os
import hashlib
import re
from pathlib import Path


# =========================
# PATH
# =========================
KB_PATH = Path("data/knowledge/base.txt")
KB_PATH.parent.mkdir(parents=True, exist_ok=True)


# =========================
# NORMALIZER
# =========================
def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)  # remove symbol
    return text


# =========================
# HASH KEY (ANTI DUPLICATE)
# =========================
def make_key(q, a):
    return hashlib.md5(f"{q}|{a}".encode()).hexdigest()


# =========================
# VALIDATOR (FILTER SAMPAH)
# =========================
def is_valid(q, a):
    blacklist = [
        "error",
        "gagal",
        "unknown",
        "none",
        "tidak tahu"
    ]

    if len(q) < 2 or len(a) < 2:
        return False

    if any(b in a.lower() for b in blacklist):
        return False

    if len(q) > 80 or len(a) > 200:
        return False

    return True


# =========================
# LOAD EXISTING KEYS
# =========================
def load_existing():
    keys = set()

    if not KB_PATH.exists():
        return keys

    with open(KB_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                q, a = line.strip().split("|", 1)
                keys.add(make_key(q, a))

    return keys


# =========================
# ADD KNOWLEDGE (MAIN FUNCTION)
# =========================
def add_knowledge(question, answer):
    question = normalize(question)
    answer = answer.strip()

    if not is_valid(question, answer):
        return False

    key = make_key(question, answer)
    existing = load_existing()

    if key in existing:
        return False  # duplicate

    with open(KB_PATH, "a", encoding="utf-8") as f:
        f.write(f"{question}|{answer}\n")

    return True