import re

class CommandAI:

    def generate(self, text):
        t = text.lower().strip()
        cmds = []

        name = self._extract_name(t)

        if "buka storage" in t:
            cmds += [
                "termux-setup-storage",
                "ls ~/storage",
                "cd ~/storage/shared"
            ]

        if any(x in t for x in ["lihat file", "list file", "cek file"]):
            cmds += ["ls", "ls -la", "ls -lh"]

        if "buat file" in t and name:
            cmds += [
                f"touch {name}",
                f"echo '' > {name}"
            ]

        if "hapus file" in t and name:
            cmds += [
                f"rm {name}",
                f"rm -f {name}"
            ]

        if "install" in t and name:
            cmds += [
                f"pkg install {name} -y",
                f"apt install {name