from collections import namedtuple

def method_tampilkan_info(cls):
    def tampilkan_info(self):
        print("Nama :", self.nama)
        print("Nama anak:")
        for i, anak in enumerate(self.anak, start=1):
            print(f"{i}. {anak}")
    cls.tampilkan_info = tampilkan_info
    return cls

@method_tampilkan_info
class Orang(namedtuple("OrangBase", "nama anak")):
    pass

# Contoh penggunaan
john = Orang("John Doe", ["Timmy", "Jimmy", "Tina"])
john.tampilkan_info()

