class Person:
    sehat = False  # class attribute

    def dinyatakan_sehat(self):
        self.sehat = True  # instance attribute

joni = Person()
eko = Person()

joni.dinyatakan_sehat()
print("Joni sehat: ", joni.sehat)  # nilai Terbarui
print("Eko sehat: ", eko.sehat)    # nilai default
