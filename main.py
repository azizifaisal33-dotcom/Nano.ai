import json
import requests
from config import config

def chat_with_nano(prompt):
    payload = {
        "model": config.AI_MODEL,
        "messages": [
            {"role": "system", "content": config.get_core_instruction()},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    
    try:
        response = requests.post(config.ENDPOINT, json=payload)
        response.raise_for_status()
        return response.json()['message']['content']
    except Exception as e:
        return f"Error: Pastikan Ollama aktif di {config.LOCAL_HOST}:{config.LOCAL_PORT}"

def main():
    print(f"--- {config.AGENT_NAME} v{config.VERSION} ---")
    print(f"Welcome back, {config.OWNER_NAME}!\n")
    
    while True:
        user_input = input("you> ")
        if user_input.lower() in ["exit", "quit", "keluar"]:
            print("Sampai jumpa, Yeshie!")
            break
            
        response = chat_with_nano(user_input)
        print(f"\n🧠 {config.AGENT_NAME}:")
        print(f"{response}\n")

if __name__ == "__main__":
    main()
