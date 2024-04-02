import numpy as np
from math import tan
import pygame
from pygame import Surface
from vertex import Vertex
from line import Line

WHITE_COLOR = (255, 255, 255)

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

    def draw_scene(self, screen: Surface) -> None:
        for line in self.lines:
            self.__project_line(line, screen)

    def __create_projection_matrix(self, aspect_ratio: float, fov: float, near: float, far: float) -> np.ndarray:
        return np.array([
            [1 / (aspect_ratio * tan(fov / 2)), 0, 0, 0],
            [0, 1 / tan(fov / 2), 0, 0],
            [0, 0, - (far + near) / (far - near), (-2 * far * near) / (far - near)],
            [0, 0, -1, 0]
        ])
    
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
