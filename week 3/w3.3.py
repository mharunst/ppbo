class Shape:
    def __init__(self, width):
        self.width = width

class Square(Shape):
    name = "Square"

    def get_area(self):
        return self.width ** 2

class Triangle(Shape):
    name = "Triangle"

    def __init__(self, width, height):
        super().__init__(width)
        self.height = height

    def get_area(self):
        return 0.5 * self.width * self.height

square = Square(5)
print(f"{square.name} area: {square.get_area()}") 

triangle = Triangle(5, 3)
print(f"{triangle.name} area: {triangle.get_area()}") 
