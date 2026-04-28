
import sys
import os
from core.updater import NanoUpdater
from core.nano import NanoAI

def boot_system():
    print("--- Nano.ai System Booting ---")
    
    # 1. Cek Pembaruan (Evolusi Kode)
    updater = NanoUpdater()
    try:
        if updater.evolve_system():
            # Jika ada update, restart otomatis
            updater.restart_nano()
    except Exception as e:
        print(f"[!] Gagal mengecek update: {e}")

    # 2. Inisialisasi Otak AI
    print("[*] Memuat memori dan sistem...")
    bot = NanoAI()
    
    # 3. Jalankan Antarmuka (CLI)
    bot.start_shell()

if __name__ == "__main__":
    try:
        boot_system()
    except KeyboardInterrupt:
        print("\n[!] NanoAI dinonaktifkan. Sampai jumpa, Yeshie.")
        sys.exit(0)
