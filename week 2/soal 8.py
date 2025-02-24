class Mobil:
    def __init__(self, merk, model, tahun):
        self.merk = merk
        self.model = model
        self.tahun = tahun

    def info(self):
        print(f"Mobil {self.merk} {self.model} tahun {self.tahun}")

# Membuat objek mobil
mobil1 = Mobil("Toyota", "Corolla", 2020)
mobil2 = Mobil("Honda", "Civic", 2022)

# Menampilkan informasi mobil
mobil1.info()
mobil2.info()
