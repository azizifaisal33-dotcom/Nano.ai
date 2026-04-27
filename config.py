def find_model(self):
    paths = [
        "./models/model.gguf",
        "./model.gguf"
    ]

    for p in paths:
        if os.path.exists(p):
            return p

    # 🔥 TAMBAHAN: folder llm
    if os.path.isdir("./llm"):
        for f in os.listdir("./llm"):
            if f.endswith(".gguf"):
                return os.path.join("./llm", f)

    return None