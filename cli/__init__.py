"""
💻 Nano CLI Framework v2
"""
__version__ = "2.0.0"

# Lazy imports - Production style
def get_shell(ai_instance):
    from .shell import NanoShell
    return NanoShell(ai_instance)

def run_cli():
    from .runner import main
    main()

__all__ = ["get_shell", "run_cli"]

print("💻 CLI Framework loaded ✓")
