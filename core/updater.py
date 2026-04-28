import subprocess
import os
import sys
from config import config

class NanoUpdater:
    def __init__(self):
        self.repo_path = os.getcwd()  # Mengambil lokasi folder Nano.ai
        self.owner = config.OWNER

    def run_command(self, command):
        """Menjalankan perintah bash dan mengambil outputnya"""
        try:
            result = subprocess.run(
                command, shell=True, check=True, 
                capture_output=True, text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

    def check_for_updates(self):
        """Cek apakah ada perubahan di GitHub"""
        print(f"[*] Menghubungkan ke GitHub untuk proyek {self.owner}...")
        self.run_command("git fetch")
        local_hash = self.run_command("git rev-parse HEAD")
        remote_hash = self.run_command("git rev-parse @{u}")

        if local_hash != remote_hash:
            return True
        return False

    def evolve_system(self):
        """Proses download kode baru dan instalasi library"""
        if self.check_for_updates():
            print("[!] Versi baru ditemukan! Memulai proses evolusi...")
            
            # 1. Pull kode terbaru
            pull_status = self.run_command("git pull origin main")
            print(f"[+] Git Pull: {pull_status}")

            # 2. Update library (requirements.txt)
            if os.path.exists("requirements.txt"):
                print("[*] Mengupdate library yang diperlukan...")
                self.run_command("pip install -r requirements.txt")

            print("[√] Evolusi selesai. NanoAI perlu restart.")
            return True
        else:
            print("[√] NanoAI sudah dalam versi terbaru.")
            return False

    def restart_nano(self):
        """Mematikan proses sekarang dan memulai ulang main.py"""
        print("[*] Sedang merestart
