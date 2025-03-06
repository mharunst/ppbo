class Orang:
    def __init__(self, nama_depan, nama_belakang, nomer_ID):
        self.nama_depan = nama_depan
        self.nama_belakang = nama_belakang
        self.nomer_ID = nomer_ID

class Mahasiswa(Orang):
    SARJANA, MASTER, DOKTOR = range(3)
    def __init__(self, jenjang, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jenjang = jenjang
        self.matkul = []
    
    def enrol(self, mata_kuliah):
        self.matkul.append(mata_kuliah)

class Karyawan(Orang):
    TETAP, TDK_TETAP= range(2)
    def __init__(self, status, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = status

class Dosen(Karyawan):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.matkul_diajar = []

    def mengajar(self, matkul_diajar):
        self.matkul_diajar.append(matkul_diajar)

bowo = Mahasiswa(Mahasiswa.SARJANA, "Bowo", "Nugroho", "987654")
bowo.enrol("Basis Data")

rizki = Dosen( Karyawan.TETAP, "Rizki", "Setiabudi", "456789")
rizki.mengajar("Statistik")

class Pelajar:
    def __init__(self):
        self.matkul = []
    
    def enrol(self, mata_kuliah):
        self.matkul.append(mata_kuliah)

class Pengajar:
    def __init__(self):
        self.matkul_diajar = []
    
    def mengajar(self, mata_kuliah):
        self.matkul_diajar.append(mata_kuliah)

class Asdos(Orang, Pelajar, Pengajar):
    def __init__(self, nama_depan, nama_belakang, nomer_ID):
        Orang.__init__(self, nama_depan, nama_belakang, nomer_ID)
        Pelajar.__init__(self)
        Pengajar.__init__(self)

uswatun = Asdos("Uswatun", "Hasanah", "456456")
uswatun.enrol("Big Data")
uswatun.mengajar("Kecerdasan Artifisial")

def cetak():
    print(f"Nama: {uswatun.nama_depan} {uswatun.nama_belakang}")
    print(f"Nomer ID: {uswatun.nomer_ID}")
    print(f"Mata Kuliah yang diambil: {uswatun.matkul}")
    print(f"Mata Kuliah yang diajar: {uswatun.matkul_diajar}")

def cetakobjek2():
    print(f"Nama: {rizki.nama_depan} {rizki.nama_belakang}")
    print(f"Nomer ID: {rizki.nomer_ID}")
    print(f"Kode Status Karyawan: {rizki.status}")

def cetakobjek1():
    print(f"Nama: {bowo.nama_depan} {bowo.nama_belakang}")
    print(f"Nomer ID: {bowo.nomer_ID}")
    print(f"Mata Kuliah yang diambil: {bowo.matkul}")
    print(f"Kode Jenjang: {bowo.jenjang}")

cetakobjek1()
cetakobjek2()
cetak()

