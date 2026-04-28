cat > plugins/network.py << 'EOF'
#!/usr/bin/env python3
import os
import subprocess
import time
import re
from typing import Dict, List

class NetworkAgent:
    def __init__(self):
        self.auto_connect = True

    def check_wifi(self) -> Dict:
        """Auto check wifi status"""
        try:
            # Termux wifi check
            status = subprocess.getoutput("termux-wifi-connectioninfo 2>/dev/null || ping -c1 8.8.8.8")
            online = "connected" in status.lower() or "1 received" in status
            return {"status": "🟢 ONLINE" if online else "🔴 OFFLINE", "ping": status[:100]}
        except:
            return {"status": "❓ UNKNOWN"}

    def auto_connect_wifi(self) -> str:
        """Auto connect to wifi"""
        try:
            # Scan & connect (Termux:API)
            os.system("termux-wifi-scaninfo > /dev/null 2>&1")
            os.system("termux-wifi-enable true")
            time.sleep(3)
            return "📶 WiFi scanning... Connected!"
        except:
            return "📶 WiFi check: ping google.com"

    def search_google(self, query: str) -> str:
        """Auto search NO MANUAL SETUP"""
        try:
            # Curl google (NO browser needed)
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            result = subprocess.getoutput(f"curl -s -A 'NanoAI' '{url}' | grep -o 'https://[^ ]*' | head -3 | tr '\\n' '\\n'")
            if result:
                return f"🔍 {query}\n{result}"
            return f"🌐 {url}"
        except:
            return f"🔍 curl 'https://google.com/search?q={query}'"

    def process(self, cmd: str) -> str:
        cmd = cmd.lower()
        
        if "wifi" in cmd or "internet" in cmd:
            wifi = self.check_wifi()
            if wifi["status"] == "🔴 OFFLINE":
                self.auto_connect_wifi()
            return f"📶 {wifi['status']}"
        
        if "cari" in cmd or "search" in cmd:
            query = cmd.split("cari", 1)[-1].split("search", 1)[-1].strip()
            return self.search_google(query)
        
        return "network: wifi | cari 'query'"

network = NetworkAgent()
EOF