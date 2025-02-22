class Anime:
    def __init__(self, judul, author):  
        self.judul = judul
        self.author = author

    def tampilkan_info(self):
        print(f"Judul: {self.judul}, Author: {self.author}")

anime1 = Anime("Naruto", "Masashi Kishimoto")  
anime2 = Anime("One Piece", "Eiichiro Oda")

anime1.tampilkan_info()
anime2.tampilkan_info()
