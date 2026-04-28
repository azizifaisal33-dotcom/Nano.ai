import struct
import os
from pathlib import Path
from core.math_utils import NanoMath

class RevolverIO:
    @staticmethod
    def save_lvr(file_path, weights, version=1):
        # Pastikan folder tempat menyimpan file sudah ada
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb') as f:
            # Header: RVR (3 bytes), Version (4 bytes), Count (4 bytes)
            header = struct.pack('3sII', b'RVR', version, len(weights))
            f.write(header)
            # Mengemas semua list float menjadi biner
            binary_weights = struct.pack(f'{len(weights)}f', *weights)
            f.write(binary_weights)

    @staticmethod
    def load_lvr(file_path):
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
    def __init__(self, dna_path="data/brain.lvr", size=128):
        self.dna_path = dna_path
        self.size = size
        
        # PERBAIKAN: load_lvr mengembalikan Tuple (weights, version) atau None
        dna_data = RevolverIO.load_lvr(self.dna_path)
        
        if dna_data:
            self.weights = dna_data # Ambil bagian weights saja
            self.version = dna_data
        else:
            # Jika file tidak ada, buat inisialisasi default
            self.weights = [0.01] * self.size
            self.version = 1

    def save_dna(self):
        RevolverIO.save_lvr(self.dna_path, self.weights)

    def evolve(self, tokens, feedback_score=0.1):
        if not tokens: return
        
        # Simulasi vector dari tokens secara sederhana
        vectors = [float(hash(t) % 100) / 100 for t in tokens]
        
        # Pastikan NanoMath.softmax sudah kamu buat di core/math_utils.py
        attention_scores = NanoMath.softmax(vectors)

        for i, score in enumerate(attention_scores):
            # Update weights secara melingkar (modulo)
            idx = i % self.size
            self.weights[idx] += score * feedback_score
            
        self.save_dna()

# Global Instance
revolver = Revolver()
