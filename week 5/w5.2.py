class Kendaraan:
    def bergerak(self):
        pass

class Mobil(Kendaraan):
    def bergerak(self):
        return "Mobil berjalan di jalan raya"

class Perahu(Kendaraan):
    def bergerak(self):
        return "Perahu berlayar di laut"

obj_mobil  = Mobil()
obj_Perahu = Perahu()

# Implementasi Polimorfisme
for transport in (obj_mobil, obj_Perahu):
    print(transport.bergerak())
