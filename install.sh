#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 NANO AI INSTALLER START"

# =====================
# UPDATE TERMUX
# =====================
pkg update -y && pkg upgrade -y

# =====================
# INSTALL DEPENDENCY
# =====================
pkg install -y python git

# =====================
# PYTHON SETUP
# =====================
pip install --upgrade pip

# kalau ada requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# =====================
# PERMISSION
# =====================
chmod +x cli/runner.py

# =====================
# GLOBAL COMMAND
# =====================
cp cli/runner.py $PREFIX/bin/nanoai

echo ""
echo "✅ INSTALL SELESAI"
echo "Gunakan: nanoai"