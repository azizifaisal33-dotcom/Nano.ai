import struct
import os
from pathlib import Path
from core.math_utils import NanoMath

class RevolverIO:
    @staticmethod
    def save_lvr(file_path, weights, version=1):
        # Memastikan file_path adalah string atau Path
        str_path = str(file_path)
        os.makedirs(os.path.dirname(str_path), exist_ok=True)

        with open(str_path, 'wb') as f:
            # Header: RVR (3 bytes), Version (4 bytes), Count (4 bytes)
            header = struct.pack('3sII', b'RVR', version, len(weights))
            f.write(header)
            # Mengemas list float menjadi biner
            binary_weights = struct.pack(f'{len(weights)}f', *weights)
            f.write(binary_weights)

    @staticmethod
    def load_lvr(file_path):
        # Validasi path agar tidak error jika yang masuk adalah objek FileSystem
        if not isinstance(file_path, (str, Path)):
            return None
            
        path = Path(file_path)
        if not path.exists(): return None
        try:
            with open(path, 'rb') as f:
                header_data = f.read(11)
                if len(header_data) < 11: return None
                magic, version, count = struct.unpack('3sII', header_data)

                if magic != b'RVR': 
                    print("⚠️  Magic byte salah!")
                    return None

                weights_data = f.read(count * 4)
                if not weights_data: return None

                weights = list(struct.unpack(f'{count}f', weights_data))
                return weights, version
        except Exception as e:
            print(f"⚠️  Gagal memuat DNA: {e}")
            return None

class Revolver:
    # Ditambah fs dan backup agar sinkron dengan Brain(self.fs, self.backup)
    def __init__(self, fs=None, backup=None, dna_path="data/brain.lvr", size=128):
        self.fs = fs
        self.backup = backup
        self.dna_path = dna_path
        self.size = size

        # Load data DNA
        dna_data = RevolverIO.load_lvr(self.dna_path)

        if dna_data:
            # FIX: dna_data itu isinya (weights, version). Jangan diambil semua!
            self.weights = dna_data 
            self.version = dna_data
        else:
            self.weights = [0.01] * self.size
            self.version = 1

    def save_dna(self):
        RevolverIO.save_lvr(self.dna_path, self.weights, self.version)

    def evolve(self, tokens, feedback_score=0.1):
        if not tokens: return

        # Simulasi vector sederhana
        vectors = [float(hash(t) % 100) / 100 for t in tokens]

        # Pastikan NanoMath punya fungsi softmax!
        # Jika belum ada, gunakan rata-rata sederhana dulu agar tidak crash
        try:
            attention_scores = NanoMath.softmax(vectors)
        except AttributeError:
            # Fallback jika softmax belum dibuat
            total = sum(vectors) if sum(vectors) != 0 else 1
            attention_scores = [v / total for v in vectors]

        for i, score in enumerate(attention_scores):
            idx = i % self.size
            # Sekarang self.weights dipastikan list of float
            self.weights[idx] += score * feedback_score

        self.save_dna()

# Global Instance (Tanpa parameter untuk default)
revolver = Revolver()
