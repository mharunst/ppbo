class Mahasiswa:
    def __init__(self, nama, nim):
        self.nama = nama
        self.nim = nim

    def info(self):
        return f"Mahasiswa: {self.nama}, NIM: {self.nim}"

class Dosen:
    def __init__(self, nama, nip):
        self.nama = nama
        self.nip = nip

    def info(self):
        return f"Dosen: {self.nama}, NIP: {self.nip}"

class FactoryUser:
    @staticmethod
    def create_user(user_type, nama, id_number):
        if user_type.lower() == "mahasiswa":
            return Mahasiswa(nama, id_number)
        elif user_type.lower() == "dosen":
            return Dosen(nama, id_number)
        else:
            raise ValueError("Tipe user tidak dikenal.")

# Tes Factory
user1 = FactoryUser.create_user("mahasiswa", "Anhar", "24/530987")
user2 = FactoryUser.create_user("dosen", "Bu Anni", "19706")

print(user1.info())
print(user2.info())
