#!/bin/bash
echo "🚀 Installing NanoAI (Self-contained)..."

mkdir -p data/memory data/knowledge backups
chmod +x cli/*.py main.py
echo "✅ Ready! Run: python main.py"