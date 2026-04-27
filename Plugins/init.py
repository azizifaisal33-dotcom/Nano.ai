"""
🔌 Plugin System - Auto-discovery
"""
import importlib
import pkgutil
import os
from typing import Dict, Callable

plugins = {}

def load_plugins():
    """Auto-discover and load plugins"""
    plugin_dir = os.path.dirname(__file__)
    
    for importer, modname, ispkg in pkgutil.iter_modules([plugin_dir]):
        if modname.startswith('_'):
            continue
            
        try:
            module = importlib.import_module(f"plugins.{modname}")
            if hasattr(module, 'register'):
                plugin = module.register()
                plugins[modname] = plugin
                print(f"🔌 Loaded plugin: {modname}")
        except Exception as e:
            print(f"❌ Plugin {modname} failed: {e}")

def get_plugin(name: str) -> Callable:
    return plugins.get(name)

load_plugins()