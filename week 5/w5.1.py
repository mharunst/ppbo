class A1:
    def nama(self):
        print("Anhar")

class A2:
    def nama(self):
        print("Fauzan")

member_A1 = A1()
member_A2 = A2()

for i in (member_A1, member_A2):
    i.nama()

