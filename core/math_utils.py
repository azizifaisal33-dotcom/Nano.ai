class NanoMath:
    @staticmethod
    def tambah(list_a, list_b):
        """Menjumlahkan dua list angka"""
        return [a + b for a, b in zip(list_a, list_b)]

    @staticmethod
    def rata_rata(data_list):
        """Menghitung rata-rata dari sebuah list"""
        if not data_list: return 0
        return sum(data_list) / len(data_list)

    @staticmethod
    def normalisasi(teks):
        """Contoh fungsi buatan sendiri untuk memproses teks sederhana"""
        return teks.lower().strip()
