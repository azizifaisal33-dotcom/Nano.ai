import re

class CommandAI:

    def generate(self, text):
        t = text.lower()

        cmds = []

        # mapping dasar
        if "buka storage" in t:
            cmds += [
                "termux-setup-storage",
                "ls ~/storage",
                "cd ~/storage"
            ]

        if "lihat file" in t or "list file" in t:
            cmds += ["ls", "ls -la"]

        if "hapus file" in t:
            name = self._extract_name(t)
            if name:
                cmds += [f"rm {name}", f"rm -f {name}"]

        if "buat file" in t:
            name = self._extract_name(t)
            if name:
                cmds += [f"touch {name}", f"echo '' > {name}"]

        if "install" in t:
            pkg = self._extract_name(t)
            if pkg:
                cmds += [
                    f"pkg install {pkg} -y",
                    f"apt install {pkg} -y"
                ]

        # fallback → pakai teks asli
        if not cmds:
            cmds.append(text)

        return cmds

    def _extract_name(self, text):
        words = text.split()
        for w in words[::-1]:
            if "." in w or w.isalpha():
                return w
        return None