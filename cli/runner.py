#!/usr/bin/env python3

import sys
from cli.shell import NanoShell
from core.brain import Brain


def main():
    # kalau ada argumen → langsung eksekusi (non-interactive)
    if len(sys.argv) > 1:
        ai = Brain()
        command = " ".join(sys.argv[1:])
        result = ai.think(command)
        print(result)
        return

    # kalau tidak ada argumen → masuk shell interaktif
    shell = NanoShell()
    shell.start()


if __name__ == "__main__":
    main()