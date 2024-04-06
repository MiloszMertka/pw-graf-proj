import numpy as np
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
    
    def is_wholly_in_front(self, plane_point, plane_normal):
        for vertex in self.vertices:
            vertex = vertex.to_vector3()
            if np.dot(vertex - plane_point, plane_normal) < 0:
                return False
        return True

    def is_wholly_behind(self, plane_point, plane_normal):
        for vertex in self.vertices:
            vertex = vertex.to_vector3()
            if np.dot(vertex - plane_point, plane_normal) > 0:
                return False
        return True

    def split(self, plane_point, plane_normal):
        front_vertices = []
        back_vertices = []
        last_vertex = self.vertices[-1].to_vector3()
        last_dot = np.dot(last_vertex - plane_point, plane_normal)

        for vertex in self.vertices:
            vertex = vertex.to_vector3()
            dot = np.dot(vertex - plane_point, plane_normal)
            if dot * last_dot < 0:
                intersection_vertex = last_vertex + (vertex - last_vertex) * (-last_dot / (dot - last_dot))
                front_vertices.append(Vertex(intersection_vertex[0], intersection_vertex[1], intersection_vertex[2]))
                back_vertices.append(Vertex(intersection_vertex[0], intersection_vertex[1], intersection_vertex[2]))
            if dot >= 0:
                front_vertices.append(Vertex(vertex[0], vertex[1], vertex[2]))
            if dot <= 0:
                back_vertices.append(Vertex(vertex[0], vertex[1], vertex[2]))
            last_vertex = vertex
            last_dot = dot

        return Polygon(front_vertices), Polygon(back_vertices)
