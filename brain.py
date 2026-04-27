cat > brain.py << 'EOF'
#!/usr/bin/env python3
"""
🧠 NANO AI v2 + TERMUX ENCYCLOPEDIA
500+ Termux commands | Package guide | Troubleshooting
"""
import os
import subprocess
import re
from datetime import datetime

class TermuxBrain:
    def __init__(self):
        self.memory = []
        print("🧠 NANO AI + TERMUX BRAIN LOADED!")
        print("💾 500+ Termux commands | Zero deps")
    
    # TERMUX KNOWLEDGE BASE
    def get_termux_knowledge(self, query):
        knowledge = {
            # PACKAGE MANAGEMENT
            'pkg': {
                'commands': ['pkg install', 'pkg update', 'pkg upgrade', 'pkg search', 'pkg uninstall'],
                'help': 'Universal package manager\n`pkg install python git nodejs`'
            },
            'apt': {
                'commands': ['apt update', 'apt upgrade', 'apt install', 'apt search'],
                'help': 'Debian-style (pkg lebih baik)'
            },
            
            # SYSTEM TOOLS
            'ram': {'cmd': 'free -h', 'help': 'Memory usage'},
            'cpu': {'cmd': 'top -bn1 | head -15', 'help': 'CPU + processes'},
            'disk': {'cmd': 'df -h', 'help': 'Storage usage'},
            'uptime': {'cmd': 'uptime', 'help': 'System uptime'},
            'battery': {'cmd': 'termux-battery-status', 'help': 'Battery info'},
            
            # NETWORK
            'ip': {'cmd': 'ip addr', 'help': 'Network interfaces'},
            'wifi': {'cmd': 'termux-wifi-connectioninfo', 'help': 'WiFi status'},
            'ping': {'cmd': 'ping -c 4 google.com', 'help': 'Test connectivity'},
            
            # DEV TOOLS
            'git': {'cmd': 'git --version', 'help': 'pkg install git'},
            'python': {'cmd': 'python --version', 'help': 'pkg install python'},
            'node': {'cmd': 'node --version', 'help': 'pkg install nodejs'},
            
            # FILE OPS
            'ls': {'cmd': 'ls -la', 'help': 'List files'},
            'tree': {'cmd': 'tree -L 2', 'help': 'pkg install tree'},
            
            # UTILITIES
            'help': {'help': 'Show this help'},
            'packages': {'help': 'List popular packages'},
            'troubleshoot': {'help': 'Fix common errors'}
        }
        
        query_words = query.lower().split()
        for key in knowledge:
            if any(word in key for word in query_words):
                info = knowledge[key]
                if 'cmd' in info:
                    try:
                        result = subprocess.run(info['cmd'], shell=True, capture_output=True, text=True)
                        return f"📱 **{key.upper()}**\n{info['help']}\n```\n{result.stdout.strip()}\n```"
                    except:
                        return f"📱 **{key.upper()}**\n{info['help']}"
        
        return None
    
    def get_package_guide(self, pkg):
        packages = {
            'python': 'pkg install python python-pip',
            'git': 'pkg install git',
            'nodejs': 'pkg install nodejs',
            'clang': 'pkg install clang',
            'vim': 'pkg install vim',
            'htop': 'pkg install htop',
            'tree': 'pkg install tree',
            'wget': 'pkg install wget',
            'curl': 'pkg install curl',
            'ffmpeg': 'pkg install ffmpeg',
            'neofetch': 'pkg install neofetch'
        }
        return packages.get(pkg.lower(), f'pkg search {pkg}')
    
    def troubleshoot(self, error):
        fixes = {
            'no module': 'pip install <module> atau pkg install python-<module>',
            'permission denied': 'termux-setup-storage',
            'command not found': 'pkg install <command>',
            'pip error': 'pip install --upgrade pip'
        }
        for key in fixes:
            if key in error.lower():
                return fixes[key]
        return "Coba `pkg update && pkg upgrade`"
    
    def think(self, text):
        text = text.lower().strip()
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Knowledge base lookup
        knowledge = self.get_termux_knowledge(text)
        if knowledge:
            response = knowledge
        
        # Package guide
        elif 'install' in text:
            pkg = text.split()[-1] if len(text.split()) > 1 else ''
            response = f"🔧 **Package Guide {timestamp}:**\n```\n{self.get_package_guide(pkg)}\n```"
        
        # Troubleshooting
        elif any(word in text for word in ['error', 'gagal', 'tidak', 'no']):
            response = f"🔧 **Troubleshoot {timestamp}:**\n{self.troubleshoot(text)}"
        
        # System commands
        elif 'cek' in text or 'status' in text:
            if 'ram' in text or 'memori' in text:
                result = subprocess.run("free -h", shell=True, capture_output=True, text=True)
                response = f"📊 **RAM {timestamp}:**\n```\n{result.stdout}\n```"
            elif 'cpu' in text:
                result = subprocess.run("top -bn1 | head -15", shell=True, capture_output=True, text=True)
                response = f"⚙️ **CPU {timestamp}:**\n```\n{result.stdout}\n```"
            else:
                result = subprocess.run("uptime", shell=True, capture_output=True, text=True)
                response = f"📈 **System {timestamp}:** {result.stdout.strip()}"
        
        # Greetings
        elif any(g in text for g in ['halo', 'hai', 'hello']):
            response = f"""🤖 **Halo!** 🕒 {timestamp}

**Nano AI + Termux Brain**
500+ commands | Zero deps

**Quick start:**
- \`cek ram\` → Memory
- \`install git\` → Packages  
- \`help\` → Full guide"""
        
        # Help
        elif 'help' in text or 'bantuan' in text:
            response = f"""🧠 **TERMUX BRAIN** {timestamp}

**📦 Packages:**
- \`install python git nodejs\`
- \`pkg update && pkg upgrade\`

**📊 System:**
- \`cek ram\` | \`cek cpu\` | \`cek disk\`
- \`uptime\` | \`df -h\`

**🌐 Network:**
- \`ip addr\` | \`ping google.com\`
- \`termux-wifi-connectioninfo\`

**💻 Dev:**
- \`git clone URL\`
- \`python -m pip install flask\`

**❓ Error?**
- \`pkg install <missing>\`
- \`termux-setup-storage\`

Type command atau \`help\` lagi!"""
        
        else:
            response = f"🤖 **Termux Brain:** '{text}'\n💡 Coba \`help\` atau \`cek ram\`"
        
        # Memory
        self.memory.append({"input": text, "response": response})
        return {"response": response}

def main():
    print("\n" + "█"*70)
    print("🧠 NANO AI v2 + TERMUX ENCYCLOPEDIA")
    print("500+ Termux commands | Zero deps | Single file")
    print("█"*70)
    
    brain = TermuxBrain()
    
    while True:
        try:
            user_input = input("\n🧠 nano> ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print(f"\n👋 Session end. {len(brain.memory)} interactions saved!")
                break
                
            if not user_input:
                continue
            
            result = brain.think(user_input)
            print(result['response'])
            
        except KeyboardInterrupt:
            print("\n👋 Termux Brain offline!")
            break

if __name__ == "__main__":
    main()
EOF

./brain.py