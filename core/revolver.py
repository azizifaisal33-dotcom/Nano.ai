import os

class Revolver:
    def __init__(self, fs, backup):
        self.fs = fs
        self.backup = backup

    def evolve(self, file, instr):
        if not os.path.exists(file):
            return "file tidak ditemukan"

        self.backup.create()

        code = self.fs.read(file)

        if "debug" in instr:
            code = "print('DEBUG')\n" + code

        if "fix none" in instr:
            code = code.replace("== None", "is None")

        self.fs.write(file, code)

        return f"🧬 evolve: {file}"