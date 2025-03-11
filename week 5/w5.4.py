class Gudang:
    def __init__(self, nama_barang, stok):
        self.nama_barang = nama_barang
        self.stok = stok  # dalam liter

    def __sub__(self, pesanan):
        print(f"Jumlah pesanan: {pesanan.jumlah_pesan} liter")
        return self.stok - pesanan.jumlah_pesan


class Pesanan:
    def __init__(self, nama_barang, jumlah_pesan):
        self.nama_barang = nama_barang
        self.jumlah_pesan = jumlah_pesan


# Objek Gudang
minyak_goreng = Gudang("Minyak Goreng", 1000)  # Stok awal = 1000 liter
# Objek Pesanan
pesanan_pelanggan = Pesanan("Minyak Goreng", 350)  # Pelanggan membeli 350 liter

# Menghitung sisa stok setelah pembelian
sisa_stok = minyak_goreng - pesanan_pelanggan
print(f"Sisa stok {minyak_goreng.nama_barang} di gudang: {sisa_stok} liter")

