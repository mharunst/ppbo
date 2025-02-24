class Buku:
    def __init__(self, judul, penulis):
        self.judul = judul
        self.penulis = penulis

    def info(self):
        return (f"Judul Buku : {self.judul}\nPenulis    : {self.penulis}")

# Membuat objek buku
buku1 = Buku("Harry Potter", "J.K. Rowling")
buku2 = Buku("Laskar Pelangi", "Andrea Hirata")

# Output
print(buku1.info())
print(buku2.info())
