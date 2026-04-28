import subprocess
import os
import sys

class NanoUpdater:
    def __init__(self):
        self.repo_path = os.getcwd()

    def run_command(self, command):
        """Menjalankan perintah bash dengan aman"""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def check_for_updates(self):
        """Cek update ke GitHub tanpa memutus program"""
        print("[*] Mengecek pembaruan sistem...")
        # Pastikan ini adalah folder git
        if not os.path.exists(".git"):
            return False
            
        self.run_command("git fetch")
        local = self.run_command("git rev-parse HEAD")
        remote = self.run_command("git rev-parse @{u}")
        
        return local != remote

    def evolve_system(self):
        """Proses pembaruan otomatis (Evolve)"""
        try:
            if self.check_for_updates():
                print("[!] Versi baru ditemukan. Memulai evolusi kode...")
                self.run_command("git pull origin main")
                
                if os.path.exists("requirements.txt"):
                    self.run_command("pip install -r requirements.txt")
                
                print("[√] Evolusi sukses.")
                return True
            else:
                print("[√] Sistem sudah dalam versi terbaru.")
                return False
        except:
            print("[!] Gagal melakukan update. Cek koneksi internet.")
            return False

    def restart_nano(self):
        """Restart otomatis untuk menerapkan perubahan"""
        print("[*] Memulai ulang sistem untuk menerapkan update...")
        os.execv(sys.executable, ['python'] + sys.argv)

# Inisialisasi sederhana
updater = NanoUpdater()
