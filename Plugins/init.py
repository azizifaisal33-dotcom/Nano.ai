"""
🔌 Nano AI Plugin System v2.1 - Auto-discovery + Hot Reload
Advanced plugin manager with error recovery
"""
import importlib
import pkgutil
import os
import sys
from typing import Dict, Callable, List, Optional
from pathlib import Path
import importlib.util
from rich.console import Console
from rich.table import Table

console = Console()
plugins: Dict[str, Dict] = {}
plugin_errors: List[str] = []

def load_plugins():
    """Auto-discover and load plugins with error recovery"""
    global plugins, plugin_errors
    plugins.clear()
    plugin_errors.clear()
    
    plugin_dir = Path(__file__).parent
    console.print(f"[blue]🔌 Scanning {plugin_dir}...[/]")
    
    # Scan Python modules
    for importer, modname, ispkg in pkgutil.iter_modules([str(plugin_dir)]):
        if modname.startswith('_'):
            continue
            
        try:
            module = importlib.import_module(f"plugins.{modname}")
            if hasattr(module, 'register'):
                plugin_info = module.register()
                plugins[modname] = plugin_info
                console.print(f"[green]✅ Loaded[/] [bold cyan]{modname}[/]: {plugin_info.get('description', 'No desc')}")
            else:
                plugin_errors.append(f"{modname}: No register() function")
        except Exception as e:
            error_msg = f"{modname}: {str(e)}"
            plugin_errors.append(error_msg)
            console.print(f"[red]❌ {error_msg}[/]")
    
    # Summary
    console.print(f"\n[bold green]Plugin Summary:[/] {len(plugins)} loaded, {len(plugin_errors)} errors")
    
    if plugin_errors:
        console.print("[yellow]Errors (non-fatal):[/]")
        for error in plugin_errors[:3]:  # First 3
            console.print(f"  • {error}")

def get_plugin(name: str) -> Optional[Dict]:
    """Get plugin info"""
    return plugins.get(name)

def list_plugins() -> List[str]:
    """List all loaded plugins"""
    return list(plugins.keys())

def get_commands() -> Dict[str, Callable]:
    """Get all plugin commands"""
    commands = {}
    for plugin_name, plugin_info in plugins.items():
        if 'commands' in plugin_info:
            for cmd_name, cmd_func in plugin_info['commands'].items():
                commands[f"{plugin_name}.{cmd_name}"] = cmd_func
    return commands

def reload_plugin(plugin_name: str) -> bool:
    """Hot reload single plugin"""
    try:
        importlib.reload(sys.modules[f"plugins.{plugin_name}"])
        load_plugins()  # Reload all
        console.print(f"[green]🔄 Reloaded {plugin_name}[/]")
        return True
    except Exception as e:
        console.print(f"[red]❌ Reload failed: {e}[/]")
        return False

def show_plugins_table():
    """Rich plugin table"""
    table = Table(title="🔌 Loaded Plugins")
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Commands", justify="right")
    
    for name, info in plugins.items():
        cmd_count = len(info.get('commands', {}))
        table.add_row(
            name,
            info.get('description', 'No description'),
            str(cmd_count)
        )
    
    console.print(table)

# Auto-load on import
load_plugins()

# Global access
__all__ = ["load_plugins", "get_plugin", "list_plugins", "get_commands", "reload_plugin", "show_plugins_table"]