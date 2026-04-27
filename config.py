import os


class Config:
    def __init__(self):
        self.debug = True
        self.model_path = self.find_model()

    def find_model(self):
        # models folder
        if os.path.exists("./models/model.gguf"):
            return "./models/model.gguf"

        # llm folder (punyamu)
        if os.path.isdir("./llm"):
            for f in os.listdir("./llm"):
                if f.endswith(".gguf"):
                    return os.path.join("./llm", f)

        # fallback root
        if os.path.exists("./model.gguf"):
            return "./model.gguf"

        return None


# 🔥 INI YANG PENTING (WAJIB ADA)
config = Config()