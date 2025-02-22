class Manusia:

    def __init__(self, nama, umur):
        self.nama = nama  
        self.umur = umur  

    def tampilkan_data(self):
        print(f"Nama: {self.nama}")
        print(f"Umur: {self.umur} tahun")

nama = input("Masukkan nama: ")
umur = int(input("Masukkan umur: ")) 

manusia1 = Manusia(nama, umur)

manusia1.tampilkan_data()