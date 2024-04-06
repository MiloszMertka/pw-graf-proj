import numpy as np
from vertex import Vertex

WHITE_COLOR = (255, 255, 255)

class Polygon:
    def __init__(self, vertices: list[Vertex]) -> None:
        self.vertices = vertices
        self.color = WHITE_COLOR

    def set_color(self, color: tuple[int, int, int]) -> None:
        self.color = color
    
    def is_wholly_in_front(self, plane_point: np.ndarray, plane_normal: np.ndarray) -> bool:
        for vertex in self.vertices:
            vertex = vertex.to_vector3()
            if np.dot(vertex - plane_point, plane_normal) < 0:
                return False
        return True

    def is_wholly_behind(self, plane_point: np.ndarray, plane_normal: np.ndarray) -> bool:
        for vertex in self.vertices:
            vertex = vertex.to_vector3()
            if np.dot(vertex - plane_point, plane_normal) > 0:
                return False
        return True

    def split_by_plane(self, plane_point: np.ndarray, plane_normal: np.ndarray) -> tuple['Polygon', 'Polygon']:
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
    
    def calculate_plane(self) -> tuple[np.ndarray, np.ndarray]:
        plane_point = self.vertices[0].to_vector3()
        plane_normal = np.cross(self.vertices[1].to_vector3() - plane_point, self.vertices[2].to_vector3() - plane_point)
        return plane_point, plane_normal
