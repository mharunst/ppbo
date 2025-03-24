def add_info_method(cls):
    def info(self):
        print(f"Judul Buku : {self.judul}\nPenulis    : {self.penulis}")
    
    cls.info = info  # Menambahkan metode ke dalam kelas
    return cls  # Mengembalikan kelas yang sudah dimodifikasi

# Menggunakan decorator pada class
@add_info_method
class Buku:
    def __init__(self, judul, penulis):
        self.judul = judul
        self.penulis = penulis

# Membuat objek dari kelas Person
book1 = Buku("Laskar Pelangi","Andrea Hirata")

# Memanggil metode yang ditambahkan oleh decorator
book1.info()
