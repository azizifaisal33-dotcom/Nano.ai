class GitHubManager:
    def __init__(self, mode="cli"):
        self.mode = mode

    def create_repo(self, name):
        import os
        if self.mode == "cli":
            os.system(f"gh repo create {name} --public --source=. --push")
        else:
            print("Token mode aktif (implement API)")