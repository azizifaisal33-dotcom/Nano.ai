import os

class Revolver:
    def __init__(self, fs, backup):
        self.fs = fs
        self.backup = backup

    def evolve(self, file, instruction):
        if not os.path.exists(file):
            return "file tidak ditemukan"

        # 🔒 backup dulu (penting)
        try:
            self.backup.create()
        except:
            pass

        code = self.fs.read(file)

        # =========================
        # RULE PATCH (AMAN)
        # =========================
        new_code = code

        # debug mode
        if "debug" in instruction:
            if "print('DEBUG')" not in code:
                new_code = "print('DEBUG MODE')\n" + new_code

        # fix None
        if "fix none" in instruction:
            new_code = new_code.replace("== None", "is None")

        # optimize loop
        if "optimize" in instruction:
            new_code = new_code.replace("range(0,", "range(")

        # tambah log sederhana
        if "log" in instruction:
            new_code += "\nprint('LOG: executed')\n"

        # =========================
        # SIMPAN
        # =========================
        if new_code != code:
            self.fs.write(file, new_code)
            return f"🧬 evolve sukses: {file}"

        return "tidak ada perubahan"