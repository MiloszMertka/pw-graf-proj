import numpy as np

class Vertex:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = 1

    def to_vector4(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z, self.w])
    
    def to_vector3(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])
