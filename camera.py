import numpy as np
from math import tan, sin, cos
import pygame
from pygame import Surface
from vertex import Vertex
from polygon import Polygon

WHITE_COLOR = (255, 255, 255)
MOVE_STEP = 0.1
ROTATE_STEP = 0.1
ZOOM_STEP = 0.1

class Camera:
    def __init__(self, polygons: list[Polygon], fov: float, near: float, far: float, width: int, height: int, scaling_factor: int = 100) -> None:
        self.polygons = polygons
        self.fov = fov
        self.near = near
        self.far = far
        self.width = width
        self.height = height
        self.scaling_factor = scaling_factor
        self.aspect_ratio = width / height
        self.screen_center = [width / 2, height / 2]
        self.projection_matrix = self.__create_projection_matrix(self.aspect_ratio, fov, near, far)

    def move_up(self):
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.y += MOVE_STEP

    def move_down(self):
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.y -= MOVE_STEP

    def move_left(self):
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.x -= MOVE_STEP

    def move_right(self):
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.x += MOVE_STEP

    def move_forward(self):
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.z -= MOVE_STEP

    def move_backward(self):
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.z += MOVE_STEP

    def rotate_x_positive(self):
        rotation_matrix = self.__create_rotate_x_matrix(ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def rotate_x_negative(self):
        rotation_matrix = self.__create_rotate_x_matrix(-ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def rotate_y_positive(self):
        rotation_matrix = self.__create_rotate_y_matrix(ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def rotate_y_negative(self):
        rotation_matrix = self.__create_rotate_y_matrix(-ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def rotate_z_positive(self):
        rotation_matrix = self.__create_rotate_z_matrix(ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def rotate_z_negative(self):
        rotation_matrix = self.__create_rotate_z_matrix(-ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def zoom_in(self):
        self.fov -= ZOOM_STEP
        self.projection_matrix = self.__create_projection_matrix(self.aspect_ratio, self.fov, self.near, self.far)

    def zoom_out(self):
        self.fov += ZOOM_STEP
        self.projection_matrix = self.__create_projection_matrix(self.aspect_ratio, self.fov, self.near, self.far)

    def draw_scene(self, screen: Surface) -> None:
        for polygon in self.polygons:
            clipped_polygon = self.__clip_polygon(polygon)
            points = []
            for vertex in clipped_polygon.vertices:
                if vertex is None:
                    continue
                point = self.__project_point(vertex)
                self.__apply_scaling_factor(point)
                self.__move_to_screen_center(point)
                points.append(point)
            self.__draw_polygon(points, screen)

    def __rotate_polygons(self, rotation_matrix: np.ndarray) -> None:
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                self.__rotate_vertex(vertex, rotation_matrix)

    def __rotate_vertex(self, vertex: Vertex, rotation_matrix: np.ndarray) -> None:
        v = vertex.to_vector()
        rotated_v = rotation_matrix @ v
        normalized_v = self.__normalize_vector(rotated_v)
        vertex.x = normalized_v[0]
        vertex.y = normalized_v[1]
        vertex.z = normalized_v[2]

    def __create_rotate_x_matrix(self, angle: float) -> np.ndarray:
        return np.array([
            [1, 0, 0, 0],
            [0, cos(angle), -sin(angle), 0],
            [0, sin(angle), cos(angle), 0],
            [0, 0, 0, 1]
        ])
    
    def __create_rotate_y_matrix(self, angle: float) -> np.ndarray:
        return np.array([
            [cos(angle), 0, sin(angle), 0],
            [0, 1, 0, 0],
            [-sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]
        ])
    
    def __create_rotate_z_matrix(self, angle: float) -> np.ndarray:
        return np.array([
            [cos(angle), -sin(angle), 0, 0],
            [sin(angle), cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def __create_projection_matrix(self, aspect_ratio: float, fov: float, near: float, far: float) -> np.ndarray:
        return np.array([
            [1 / (aspect_ratio * tan(fov / 2)), 0, 0, 0],
            [0, 1 / tan(fov / 2), 0, 0],
            [0, 0, - (far + near) / (far - near), (-2 * far * near) / (far - near)],
            [0, 0, -1, 0]
        ])
    
    def __clip_polygon(self, polygon: Polygon) -> Polygon:
        clipped_vertices = []
        for i in range(len(polygon.vertices)):
            v1_index = i
            v2_index = (i + 1) % len(polygon.vertices)
            v1 = polygon.vertices[v1_index]
            v2 = polygon.vertices[v2_index]
            if v1.z >= self.near and v2.z >= self.near:
                clipped_vertices.append(v2)
            elif v1.z < self.near and v2.z < self.near:
                continue
            elif v1.z < self.near and v2.z >= self.near:
                intersection_point = self.__calculate_intersection_point(v1, v2)
                clipped_vertices.append(intersection_point)
                clipped_vertices.append(v2)
            elif v1.z >= self.near and v2.z < self.near:
                intersection_point = self.__calculate_intersection_point(v1, v2)
                clipped_vertices.append(intersection_point)
        return Polygon(clipped_vertices)
    
    def __calculate_intersection_point(self, v1: Vertex, v2: Vertex) -> Vertex:
        t = (self.near - v1.z) / (v2.z - v1.z)
        intersection_point = [v1.x + t * (v2.x - v1.x),
                            v1.y + t * (v2.y - v1.y),
                            self.near]
        return Vertex(intersection_point[0], intersection_point[1], intersection_point[2])

    def __project_point(self, point: Vertex) -> np.ndarray:
        vector = point.to_vector()
        projected_vector = self.projection_matrix @ vector
        normalized_vector = self.__normalize_vector(projected_vector)
        return self.__convert_vector_to_point(normalized_vector)
    
    def __normalize_vector(self, vector: np.ndarray) -> np.ndarray:
        return vector / vector[3]
    
    def __convert_vector_to_point(self, vector: np.ndarray) -> np.ndarray:
        temp_vector = vector / vector[2]
        return temp_vector[:2]
    
    def __apply_scaling_factor(self, point: np.ndarray) -> None:
        point *= self.scaling_factor
    
    def __move_to_screen_center(self, point: np.ndarray) -> None:
        point += self.screen_center

    def __draw_polygon(self, points: list[np.ndarray], screen: Surface) -> None:
        if len(points) < 2:
            return
        pygame.draw.polygon(screen, WHITE_COLOR, points, 1)
