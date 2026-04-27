import re

class CommandAI:

    def generate(self, text):
        t = text.lower().strip()
        cmds = []

        name = self._extract_name(t)

        # ======================
        # STORAGE
        # ======================
        if "buka storage" in t:
            cmds += [
                "termux-setup-storage",
                "ls ~/storage",
                "cd ~/storage/shared"
            ]

        # ======================
        # LIST FILE
        # ======================
        if any(x in t for x in ["lihat file", "list file", "cek file"]):
            cmds += ["ls", "ls -la", "ls -lh"]

        # ======================
        # BUAT FILE
        # ======================
        if "buat file" in t and name:
            cmds += [
                f"touch {name}",
                f"echo '' > {name}"
            ]

        # ======================
        # HAPUS FILE
        # ======================
        if "hapus file" in t and name:
            cmds += [
                f"rm {name}",
                f"rm -f {name}"
            ]

        # ======================
        # INSTALL
        # ======================
        if "install" in t and name:
            cmds += [
                f"pkg install {name} -y",
                f"apt install {name} -y"
            ]

        # ======================
        # JALANKAN FILE
        # ======================
        if "jalankan" in t and name:
            if name.endswith(".py"):
                cmds.append(f"python {name}")
            elif name.endswith(".sh"):
                cmds.append(f"bash {name}")

        # ======================
        # NETWORK
        # ======================
        if "cek internet" in t:
            cmds += [
                "ping -c 1 google.com",
                "curl -I https://google.com"
            ]

        # ======================
        # FALLBACK
        # ======================
        if not cmds:
            cmds.append(text)

        return self._unique(cmds)

    # =========================
    # EKSTRAKSI NAMA
    # =========================
    def _extract_name(self, text):
        match = re.findall(r"\b[\w\-]+\.\w+\b", text)
        if match:
            return match[-1]

        words = text.split()
        for w in reversed(words):
            if len(w) > 2:
                return w

        return None

    # =========================
    # HAPUS DUPLIKAT
    # =========================
    def _unique(self, cmds):
        seen = set()
        out = []
        for c in cmds:
            if c not in seen:
                seen.add(c)
                out.append(c)
        return out