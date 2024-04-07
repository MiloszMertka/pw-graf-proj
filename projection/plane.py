import numpy as np
from vertex import Vertex

class Plane:
    def __init__(self, point: np.ndarray, normal: np.ndarray) -> None:
        self.point = point
        self.normal = normal
    
    def distance_to_vertex(self, vertex: Vertex) -> float:
        vertex_vector = vertex.to_vector3()
        return np.dot(self.point - vertex_vector, self.normal)
        