class Sekolah:
    def __init__(self, Nama, NPSN, Provinsi):
        self.NamaSekolah = Nama   
        self.NPSN = NPSN          
        self.Provinsi = Provinsi 

    def tampilkan_data(self):
        print("Nama Sekolah : " + self.NamaSekolah)
        print("NPSN : " + str(self.NPSN))
        print("Provinsi : " + str(self.Provinsi))

Sekolah1 = Sekolah("SMAN 3 Bojonegoro", "20504479", "Jawa Timur")
Sekolah2 = Sekolah("MAN 3 Yogyakarta", "20411891", "D.I.Yogyakarta")
Sekolah3 = Sekolah("SMAN 1 Yogyakarta", "20403174", "D.I.Yogyakarta")
Sekolah4 = Sekolah("SMAN 1 Wonogiri", "20311334", "Jawa Tengah")

print("Informasi Sekolah 1:")
Sekolah1.tampilkan_data()

print("\nInformasi Sekolah 2:")
Sekolah2.tampilkan_data()

print("\nInformasi Sekolah 3:")
Sekolah3.tampilkan_data()

print("\nInformasi Sekolah 4:")
Sekolah4.tampilkan_data()