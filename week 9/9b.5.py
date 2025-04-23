from collections import namedtuple

# Membuat namedtuple dengan nama Buku dan field: judul, penulis, tahun
Buku = namedtuple("Buku", "judul penulis tahun")

# Membuat beberapa instance dari namedtuple Buku
buku1 = Buku("Laskar Pelangi", "Andrea Hirata", 2005)
buku2 = Buku("Negeri 5 Menara", "Ahmad Fuadi", 2009)
buku3 = Buku("Bumi", "Tere Liye", 2014)

# Menyimpan semua buku dalam list
daftar_buku = [buku1, buku2, buku3]

# Menampilkan data semua buku
print("Daftar Buku Perpustakaan:")
for buku in daftar_buku:
    print(f"Judul : {buku.judul}")
    print(f"Penulis : {buku.penulis}")
    print(f"Tahun Terbit : {buku.tahun}")
    print("-" * 30)

