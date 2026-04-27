import os


class Config:
    def __init__(self):
        self.debug = True
        self.model_path = self.find_model()

    def find_model(self):
        # prioritas file langsung
        if os.path.exists("./models/model.gguf"):
            return "./models/model.gguf"

        if os.path.exists("./model.gguf"):
            return "./model.gguf"

        # scan folder models
        if os.path.isdir("./models"):
            for f in os.listdir("./models"):
                if f.endswith(".gguf"):
                    return os.path.join("./models", f)

        return None


config = Config()