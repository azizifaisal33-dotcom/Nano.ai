#!/usr/bin/env python3
"""
🚀 CLI Runner v2 - Production Entry Point
Lazy imports for Termux compatibility
"""
import sys
import argparse
import os

# Lazy imports - Termux safe
def get_nano_ai():
    from core import get_nano_ai
    return get_nano_ai()

def get_memory():
    from core import get_memory
    return get_memory()

def get_shell(ai_instance):
    from cli import get_shell
    return get_shell(ai_instance)

def parse_args():
    parser = argparse.ArgumentParser(description="🧠 Nano AI v2 Neural Brain")
    parser.add_argument('--shell', '-s', action='store_true', help="Interactive shell")
    parser.add_argument('--query', '-q', help="Single query mode")
    parser.add_argument('--stats', action='store_true', help="Show memory stats")
    parser.add_argument('--prune', type=int, help="Prune old memory (days)")
    parser.add_argument('--reset', action='store_true', help="Reset memory DB")
    parser.add_argument('--version', '-v', action='version', version='Nano AI v2.0.0')
    return parser.parse_args()

def main():
    args = parse_args()
    
    print("🚀 Nano AI v2 Neural Brain Launcher")
    
    # Stats mode
    if args.stats:
        memory = get_memory()
        memory.show_stats()
        return
        
    # Prune mode
    if args.prune:
        memory = get_memory()
        memory.prune_old(args.prune)
        print(f"🧹 Pruned conversations older than {args.prune} days")
        return
        
    # Reset mode
    if args.reset:
        if os.path.exists("data/memory.db"):
            os.remove("data/memory.db")
            print("🔄 Memory database reset!")
        else:
            print("ℹ️ No memory database found")
        return
    
    # Single query
    if args.query:
        ai = get_nano_ai()
        result = ai.think(args.query)
        print(f"\n🤖 {result.get('response', 'Processed')}")
        return
    
    # Interactive shell (default)
    print("\n🧠 Starting Interactive Shell...")
    ai = get_nano_ai()
    shell = get_shell(ai)
    shell.simple_cli()  # Fallback to simple CLI

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Nano AI shutdown gracefully")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)