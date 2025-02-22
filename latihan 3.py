class Persegi:
    def _init_(self, sisi):
        self.sisi = sisi

    def hitung_luas(self):
        return self.sisi ** 2

    def hitung_keliling(self):
        return 4 * self.sisi

# Input panjang sisi persegi
sisi_persegi = float(input("Masukkan panjang sisi persegi: "))

# Membuat objek persegi
persegi = Persegi(sisi_persegi)

# Menampilkan hasil perhitungan
print(f"Luas persegi: {persegi.hitung_luas()} satuan luas")
print(f"Keliling persegi: {persegi.hitung_keliling()} satuan panjang")