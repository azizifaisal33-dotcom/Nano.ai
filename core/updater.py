import os
import requests
import json
import shutil
import subprocess

class NanoUpdater:
    def __init__(self, repo_url, branch="main"):
        self.repo_url = repo_url
        self.branch = branch
        self.version_file = "version.json"

    # =========================
    # CHECK VERSION
    # =========================
    def get_remote_version(self):
        try:
            url = f"{self.repo_url}/raw/{self.branch}/version.json"
            data = requests.get(url).json()
            return data["version"]
        except:
            return None


    # =========================
    # LOCAL VERSION
    # =========================
    def get_local_version(self):
        if not os.path.exists(self.version_file):
            return "0.0.0"

        return json.load(open(self.version_file))["version"]


    # =========================
    # DOWNLOAD UPDATE
    # =========================
    def download_update(self):
        print("⬇️ downloading update...")

        os.system(f"git clone {self.repo_url} update_tmp")

        return "update_tmp"


    # =========================
    # APPLY UPDATE
    # =========================
    def apply_update(self, folder):
        print("🔁 applying update...")

        for item in os.listdir(folder):
            src = os.path.join(folder, item)
            dst = os.path.join(".", item)

            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)


    # =========================
    # UPDATE SYSTEM
    # =========================
    def update(self):
        local = self.get_local_version()
        remote = self.get_remote_version()

        print(f"📌 local: {local} | remote: {remote}")

        if remote and remote != local:
            folder = self.download_update()

            self.apply_update(folder)

            print("✅ update applied")

            # cleanup
            os.system("rm -rf update_tmp")

            return True

        print("🟢 already up to date")
        return False