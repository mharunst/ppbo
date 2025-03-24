class Passenger:
    TITLES = ("Mr", "Mrs", "Ms")  # class attribute

    def __init__(self, title, fname, lname):
        if title not in self.TITLES:
            raise ValueError("%s is not a valid title." % title)

        self.title = title  # instance attribute
        self.fname = fname  # instance attribute
        self.lname = lname  # instance attribute

# Pembuatan Objek
p1 = Passenger("Mr", "Kiewlamphone", "Souvanlith")
# Mengakses class attribute dari object
print(p1.TITLES)
# Mengakses class attribute dari kelas
print(Passenger.TITLES)
# Mengakses instance attribute dari objek
print(p1.title)
# Mengakses instance attribute dari kelas (akan menyebabkan error)
print(Passenger.title)
