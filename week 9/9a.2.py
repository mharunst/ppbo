class Buku:
    jumlah_buku = 0  # variabel class untuk hitung total buku

    def __init__(self, judul, tahun_terbit):
        self.judul = judul
        self.tahun_terbit = tahun_terbit
        Buku.jumlah_buku += 1 

    @property
    def usia(self): # Menghitung usia buku
        return 2025 - self.tahun_terbit 
    
    @classmethod
    def tampilkan_jumlah(cls): # Menampilkan total buku
        print(f"Jumlah buku di perpustakaan: {cls.jumlah_buku}") 

    @staticmethod
    def cek_buku_lama(usia):
        return usia > 10 # Cek apakah buku termasuk buku lama

b1 = Buku("Laskar Pelangi", 2005)
b2 = Buku("Negeri 5 Menara", 2020)

Buku.tampilkan_jumlah()

print(f"{b1.judul} berusia {b1.usia} tahun.")

if Buku.cek_buku_lama(b1.usia):
    print(f"{b1.judul} termasuk buku lama.")
else:
    print(f"{b1.judul} termasuk buku baru.")

