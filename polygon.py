from pygame import Rect
from vertex import Vertex

WHITE_COLOR = (255, 255, 255)

class Polygon:
    def __init__(self, vertices: list[Vertex]) -> None:
        self.vertices = vertices
        self.color = WHITE_COLOR

    def set_color(self, color: tuple[int, int, int]) -> None:
        self.color = color

    def get_bounding_rectangle(self) -> Rect:
        min_x = min(self.vertices, key=lambda vertex: vertex.x).x
        max_x = max(self.vertices, key=lambda vertex: vertex.x).x
        min_y = min(self.vertices, key=lambda vertex: vertex.y).y
        max_y = max(self.vertices, key=lambda vertex: vertex.y).y
        return Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    
    def get_plane(self) -> tuple[float, float, float, float]: 
        v1 = self.vertices[0]
        v2 = self.vertices[1]
        v3 = self.vertices[2]
        a1 = v2.x - v1.x
        b1 = v2.y - v1.y
        c1 = v2.z - v1.z
        a2 = v3.x - v1.x
        b2 = v3.y - v1.y
        c2 = v3.z - v1.z
        a = b1 * c2 - b2 * c1
        b = a2 * c1 - a1 * c2
        c = a1 * b2 - b1 * a2
        d = (- a * v1.x - b * v1.y - c * v1.z)
        return a, b, c, d
    
    def get_z_centroid(self) -> float:
        return sum([vertex.z for vertex in self.vertices]) / len(self.vertices)
