"""
💻 NanoShell v2 - Rich Curses Dashboard
Advanced terminal UI with live metrics
"""
import curses
import time
import threading
from typing import Optional
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from core.nano import nano_ai
from core.memory import memory

class NanoShell:
    def __init__(self, ai):
        self.ai = ai
        self.console = Console()
        self.running = True
        self.session_history = []
        
    def run(self):
        """Main shell loop with rich UI"""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="status", size=8)
        )
        
        layout["header"].update(Panel(
            Text("🧠 Nano AI v2 Neural Brain", style="bold white on blue"),
            title="Nano AI Dashboard"
        ))
        
        # Live status table
        status_table = Table.grid(expand=True)
        status_table.add_row("Session", "Active")
        status_table.add_row("Vectors", "Loading...")
        status_table.add_row("Memory", "1.2k conv")
        
        layout["status"].update(status_table)
        
        with Live(layout, refresh_per_second=4, screen=True) as live:
            while self.running:
                # Update status
                stats = memory.get_stats()
                status_table = Table.grid(expand=True)
                status_table.add_row("Session", nano_ai.session_id[:12])
                status_table.add_row("Vectors", f"{vectorstore.index.ntotal:,}")
                status_table.add_row("Memory", f"{stats.get('total_conversations', 0):,}")
                status_table.add_row("Top Intent", stats.get('top_intents', [('',0)])[0][0])
                layout["status"].update(status_table)
                
                live.update(layout)
                time.sleep(0.5)

    def simple_cli(self):
        """Fallback simple CLI"""
        print("\n🧠 NANO AI v2 SHELL")
        print("Type 'exit', 'stats', 'memory', 'help'")
        
        while self.running:
            try:
                user_input = input("\n🧠 nano> ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("👋 Memory saved!")
                    break
                    
                if user_input.lower() == 'stats':
                    memory.show_stats()
                    continue
                    
                if user_input.lower() == 'memory':
                    memory.search_similar("ram")
                    continue
                
                # AI Processing
                result = nano_ai.think(user_input)
                nano_ai.show_thinking(result)
                
                print(f"\n🤖 {result['response']}")
                
            except KeyboardInterrupt:
                print("\n👋 Bye!")
                break

# For non-rich environments
def run_simple():
    shell = NanoShell(nano_ai)
    shell.simple_cli()