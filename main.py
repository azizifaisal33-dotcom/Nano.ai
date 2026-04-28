
from config import config
from core.engine import engine

def main():
    print(f"--- {config.AGENT_NAME} v{config.VERSION} ---")
    print(f"Welcome back, {config.OWNER_NAME}!\n")
    
    while True:
        try:
            user_input = input(f"{config.OWNER_NAME.lower()}> ")
            
            if user_input.lower() in ["exit", "quit", "keluar"]:
                print(f"Sampai jumpa, {config.OWNER_NAME}!")
                break
            
            if not user_input.strip():
                continue

            # Memanggil engine lokal secara langsung tanpa requests/http
            response = engine.generate(user_input)
            
            print(f"\n🧠 {config.AGENT_NAME}:")
            print(f"{response}\n")
            
        except KeyboardInterrupt:
            print(f"\nSistem dimatikan. Sampai jumpa, {config.OWNER_NAME}!")
            break
        except Exception as e:
            print(f"\n[!] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()
