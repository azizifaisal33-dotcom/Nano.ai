"""
🚀 CLI Runner - Entry Point
"""
import sys
import argparse
from core.nano import nano_ai
from cli.shell import NanoShell
from core.memory import memory

def parse_args():
    parser = argparse.ArgumentParser(description="🧠 Nano AI v2 Neural Brain")
    parser.add_argument('--shell', '-s', action='store_true', help="Interactive shell")
    parser.add_argument('--query', '-q', help="Single query")
    parser.add_argument('--stats', action='store_true', help="Show memory stats")
    parser.add_argument('--prune', type=int, help="Prune old memory (days)")
    parser.add_argument('--reset', action='store_true', help="Reset memory")
    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.stats:
        memory.show_stats()
        return
        
    if args.prune:
        memory.prune_old(args.prune)
        print(f"🧹 Pruned old conversations")
        return
        
    if args.reset:
        import os
        os.remove("data/memory.db")
        print("🔄 Memory reset")
        return
    
    if args.query:
        result = nano_ai.think(args.query)
        nano_ai.show_thinking(result)
        print(result['response'])
        return
    
    # Default: Interactive shell
    print("🚀 Starting Nano AI v2 Shell...")
    shell = NanoShell(nano_ai)
    shell.simple_cli()

if __name__ == "__main__":
    main()