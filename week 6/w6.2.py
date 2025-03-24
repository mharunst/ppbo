from abc import ABC, abstractmethod

class Orang(ABC):
    def __init__(self, name, NoID):
        self.name = name
        self.NoID = NoID

    @abstractmethod
    def identitas(self):
        pass  
class Mahasiswa(Orang):
    def identitas(self):
        print(f"Mahasiwa bernama {self.name} dengan NIM {self.NoID} berkuliah di UGM")
class Dosen(Orang):
    def identitas(self):
        print(f"Dosen bernama {self.name} dengan No ID {self.NoID} mengajar matakuliah Pemrograman")

mahasiwa = Mahasiswa("Anhar",538108)
dosen = Dosen("Haikal",10853)

mahasiwa.identitas()
dosen.identitas()

