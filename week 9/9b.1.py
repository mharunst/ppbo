from collections import namedtuple

Koordinat = namedtuple("Koordinat", "x y")
titik1 = Koordinat(2, 4)

# Menggunakan indeks
print("x =", titik1[0], ", y =", titik1[1])

# Menggunakan field name
print("x =", titik1.x, ", y =", titik1.y)

# Menggunakan getattr()
print("x =", getattr(titik1, 'x'), ", y =", getattr(titik1, 'y'))

