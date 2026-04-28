#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 NANO AI INSTALLER START"

# =====================
# UPDATE & REPO SETUP
# =====================
pkg update -y && pkg upgrade -y
pkg install -y x11-repo tur-repo

# =====================
# INSTALL DEPENDENCY
# =====================
pkg install -y python python-torch python-numpy libjpeg-turbo git

# =====================
# PYTHON SETUP
# =====================
pip install --upgrade pip
pip install transformers safetensors

# =====================
# DIRECTORY SETUP
# =====================
mkdir -p data/memory
mkdir -p models
touch core/__init__.py

# =====================
# PERMISSION
# =====================
chmod +x main.py

# =====================
# GLOBAL COMMAND
# =====================
# Pastikan path ini sesuai dengan file utama NanoAI kamu
cp main.py $PREFIX/bin/nanoai
chmod +x $PREFIX/bin/nanoai

echo ""
echo "✅ INSTALL SELESAI"
echo "Ketik 'nanoai' untuk menjalankan asistenmu."
