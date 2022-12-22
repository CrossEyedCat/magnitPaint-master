from MagneticVector import *


class VectorField:
    def __init__(self):
        self.collection = []

    def set_window_size(self, width: int, height: int):
        self.collection = []
        width //= 10
        height //= 10
        for i in range(width):
            for j in range(height):
                vec = Magnetic_Vector(i * 10, j * 10)
                self.collection.append(vec)

    def get_VectorField(self):
        return self.collection