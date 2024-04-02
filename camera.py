import numpy as np
from math import tan, sin, cos
import pygame
from pygame import Surface
from vertex import Vertex
from line import Line

WHITE_COLOR = (255, 255, 255)
MOVE_STEP = 0.1
ROTATE_STEP = 0.1
ZOOM_STEP = 0.1

class Camera:
    def __init__(self, lines: list[Line], fov: float, near: float, far: float, width: int, height: int, scaling_factor: int = 100) -> None:
        self.lines = lines
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
        for line in self.lines:
            line.v1.y += MOVE_STEP
            line.v2.y += MOVE_STEP

    def move_down(self):
        for line in self.lines:
            line.v1.y -= MOVE_STEP
            line.v2.y -= MOVE_STEP

    def move_left(self):
        for line in self.lines:
            line.v1.x -= MOVE_STEP
            line.v2.x -= MOVE_STEP

    def move_right(self):
        for line in self.lines:
            line.v1.x += MOVE_STEP
            line.v2.x += MOVE_STEP

    def move_forward(self):
        for line in self.lines:
            line.v1.z -= MOVE_STEP
            line.v2.z -= MOVE_STEP

    def move_backward(self):
        for line in self.lines:
            line.v1.z += MOVE_STEP
            line.v2.z += MOVE_STEP

    def rotate_x_positive(self):
        rotation_matrix = self.__create_rotate_x_matrix(ROTATE_STEP)
        self.__rotate_lines(rotation_matrix)

    def rotate_x_negative(self):
        rotation_matrix = self.__create_rotate_x_matrix(-ROTATE_STEP)
        self.__rotate_lines(rotation_matrix)

    def rotate_y_positive(self):
        rotation_matrix = self.__create_rotate_y_matrix(ROTATE_STEP)
        self.__rotate_lines(rotation_matrix)

    def rotate_y_negative(self):
        rotation_matrix = self.__create_rotate_y_matrix(-ROTATE_STEP)
        self.__rotate_lines(rotation_matrix)

    def rotate_z_positive(self):
        rotation_matrix = self.__create_rotate_z_matrix(ROTATE_STEP)
        self.__rotate_lines(rotation_matrix)

    def rotate_z_negative(self):
        rotation_matrix = self.__create_rotate_z_matrix(-ROTATE_STEP)
        self.__rotate_lines(rotation_matrix)

    def zoom_in(self):
        self.fov -= ZOOM_STEP
        self.projection_matrix = self.__create_projection_matrix(self.aspect_ratio, self.fov, self.near, self.far)

    def zoom_out(self):
        self.fov += ZOOM_STEP
        self.projection_matrix = self.__create_projection_matrix(self.aspect_ratio, self.fov, self.near, self.far)

    def draw_scene(self, screen: Surface) -> None:
        for line in self.lines:
            clipped_line = self.__clip_line(line)
            if clipped_line is not None:
                self.__project_line(clipped_line, screen)

    def __rotate_lines(self, rotation_matrix: np.ndarray) -> None:
        for line in self.lines:
            self.__rotate_vertex(line.v1, rotation_matrix)
            self.__rotate_vertex(line.v2, rotation_matrix)

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
    
    def __clip_line(self, line: Line) -> Line:
        if line.v1.z >= self.near and line.v2.z >= self.near:
            return line
        
        if line.v1.z < self.near and line.v2.z < self.near:
            return None
        
        intersection_point = self.__calculate_intersection_point(line)
        if line.v1.z < self.near:
            return Line(intersection_point, line.v2)
        else:
            return Line(line.v1, intersection_point)
    
    def __calculate_intersection_point(self, line: Line) -> Vertex:
        t = (self.near - line.v1.z) / (line.v2.z - line.v1.z)
        intersection_point = [line.v1.x + t * (line.v2.x - line.v1.x),
                            line.v1.y + t * (line.v2.y - line.v1.y),
                            self.near]
        return Vertex(intersection_point[0], intersection_point[1], intersection_point[2])
    
    def __project_line(self, line: Line, screen: Surface) -> None:
        point_v1 = self.__project_point(line.v1)
        point_v2 = self.__project_point(line.v2)
        self.__apply_scaling_factor(point_v1)
        self.__apply_scaling_factor(point_v2)
        self.__move_to_screen_center(point_v1)
        self.__move_to_screen_center(point_v2)
        self.__draw_line(point_v1[:2], point_v2[:2], screen)

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

    def __draw_line(self, start_point: np.ndarray, end_point: np.ndarray, screen: Surface) -> None:
        pygame.draw.line(screen, WHITE_COLOR, start_point, end_point)
