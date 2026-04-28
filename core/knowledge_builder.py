import re
import hashlib
from pathlib import Path


# =========================
# STORAGE PATH
# =========================
KB_PATH = Path("data/knowledge/base.txt")
KB_PATH.parent.mkdir(parents=True, exist_ok=True)


# =========================
# NORMALIZER
# =========================
def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text


# =========================
# HASH (ANTI DUPLICATE)
# =========================
def make_key(q, a):
    return hashlib.md5(f"{q}|{a}".encode()).hexdigest()


# =========================
# VALIDATOR
# =========================
def is_valid(q, a):
    blacklist = ["error", "gagal", "unknown", "none", "tidak tahu"]

    if len(q) < 2 or len(a) < 2:
        return False

    if any(b in a.lower() for b in blacklist):
        return False

    if len(q) > 100 or len(a) > 300:
        return False

    return True


# =========================
# LOAD EXISTING KEYS
# =========================
def load_existing_keys():
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
# SEARCH KNOWLEDGE
# =========================
def search_knowledge(text):
    if not KB_PATH.exists():
        return None

    text = normalize(text)

    with open(KB_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                q, a = line.strip().split("|", 1)
                if q in text:
                    return a

    return None


# =========================
# ADD KNOWLEDGE (MAIN API)
# =========================
def add_knowledge(question, answer):
    question = normalize(question)
    answer = answer.strip()

    if not is_valid(question, answer):
        return False

    key = make_key(question, answer)
    existing = load_existing_keys()

    if key in existing:
        return False

    with open(KB_PATH, "a", encoding="utf-8") as f:
        f.write(f"{question}|{answer}\n")

    return True