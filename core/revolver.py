import os
from datetime import datetime

class Evolver:
    def __init__(self, fs, backup):
        self.fs = fs
        self.backup = backup

    def evolve_file(self, file, instruction):
        if not os.path.exists(file):
            return "file tidak ditemukan"

        # backup dulu
        self.backup.create()

        code = self.fs.read(file)

        # SIMPLE PATCH LOGIC (aman)
        new_code = self._apply_patch(code, instruction)

        self.fs.write(file, new_code)

        return f"🧬 file di-evolve: {file}"

    def _apply_patch(self, code, instruction):
        # contoh rule sederhana
        if "tambah logging" in instruction:
            return "print('DEBUG MODE')\n" + code

        if "optimize" in instruction:
            return code.replace("for i in range(0,", "for i in range(")

        if "fix error" in instruction:
            return code.replace("== None", "is None")

        # default: tidak diubah
        return code