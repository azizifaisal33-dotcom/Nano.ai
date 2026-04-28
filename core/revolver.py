import struct
from pathlib import Path
from core.math_utils import NanoMath

class RevolverIO:
    @staticmethod
    def save_lvr(file_path, weights, version=1):
        with open(file_path, 'wb') as f:
            # Header: RVR (3 bytes), Version (4 bytes), Count (4 bytes)
            # Kita ganti magic byte jadi 'RVR' biar sesuai nama Revolver
            header = struct.pack('3sII', b'RVR', version, len(weights))
            f.write(header)
            binary_weights = struct.pack(f'{len(weights)}f', *weights)
            f.write(binary_weights)

    @staticmethod
    def load_lvr(file_path):
        path = Path(file_path)
        if not path.exists(): return None
        with open(path, 'rb') as f:
            header_data = f.read(11)
            if len(header_data) < 11: return None
            magic, version, count = struct.unpack('3sII', header_data)
            if magic != b'RVR': raise ValueError("File .lvr bukan format Revolver!")
            weights_data = f.read(count * 4)
            weights = list(struct.unpack(f'{count}f', weights_data))
            return weights, version

class Revolver:
    def __init__(self, dna_path="data/brain.lvr", size=128):
        self.dna_path = dna_path
        self.size = size
        dna_data = RevolverIO.load_lvr(self.dna_path)
        self.weights = dna_data if dna_data else [0.01] * self.size

    def save_dna(self):
        RevolverIO.save_lvr(self.dna_path, self.weights)

    def evolve(self, tokens, feedback_score=0.1):
        if not tokens: return
        # Proses evolusi berputar di sini
        vectors = [float(hash(t) % 100) / 100 for t in tokens]
        attention_scores = NanoMath.softmax(vectors)
        
        for i, score in enumerate(attention_scores):
            self.weights[i % self.size] += score * feedback_score
        self.save_dna()

# Global Instance
revolver = Revolver()
