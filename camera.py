import numpy as np
from math import tan, sin, cos
from functools import cmp_to_key
import pygame
from pygame import Surface, Rect
from vertex import Vertex
from polygon import Polygon
from bsp_node import BSPNode, build_bsp_tree, traverse_bsp_tree

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
        self.occlussion_enabled = True
        self.bsp_tree = build_bsp_tree(polygons)

    def toggle_occlusion(self) -> None:
        self.occlussion_enabled = not self.occlussion_enabled

    def move_up(self) -> None:
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.y += MOVE_STEP

    def move_down(self) -> None:
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.y -= MOVE_STEP

    def move_left(self) -> None:
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.x -= MOVE_STEP

    def move_right(self) -> None:
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.x += MOVE_STEP

    def move_forward(self) -> None:
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.z -= MOVE_STEP

    def move_backward(self) -> None:
        for polygon in self.polygons:
            for vertex in polygon.vertices:
                vertex.z += MOVE_STEP

    def rotate_x_positive(self) -> None:
        rotation_matrix = self.__create_rotate_x_matrix(ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def rotate_x_negative(self) -> None:
        rotation_matrix = self.__create_rotate_x_matrix(-ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def rotate_y_positive(self) -> None:
        rotation_matrix = self.__create_rotate_y_matrix(ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def rotate_y_negative(self) -> None:
        rotation_matrix = self.__create_rotate_y_matrix(-ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def rotate_z_positive(self) -> None:
        rotation_matrix = self.__create_rotate_z_matrix(ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def rotate_z_negative(self) -> None:
        rotation_matrix = self.__create_rotate_z_matrix(-ROTATE_STEP)
        self.__rotate_polygons(rotation_matrix)

    def zoom_in(self) -> None:
        self.fov -= ZOOM_STEP
        self.projection_matrix = self.__create_projection_matrix(self.aspect_ratio, self.fov, self.near, self.far)

    def zoom_out(self) -> None:
        self.fov += ZOOM_STEP
        self.projection_matrix = self.__create_projection_matrix(self.aspect_ratio, self.fov, self.near, self.far)

    def draw_scene(self, screen: Surface) -> None:
        polygons_to_draw = self.polygons[:]
        if self.occlussion_enabled:
            sorted_polygons = []
            traverse_bsp_tree(self.bsp_tree, Vertex(0, 0, 0), sorted_polygons)
            polygons_to_draw = sorted_polygons
            # polygons_to_draw.sort(key=lambda polygon: polygon.get_z_centroid(), reverse=True)
            # polygons_to_draw.sort(key=cmp_to_key(self.__compare_polygons_occlusion))
        for polygon in polygons_to_draw:
            clipped_polygon = self.__clip_polygon(polygon)
            points = []
            for vertex in clipped_polygon.vertices:
                if vertex is None:
                    continue
                point = self.__project_point(vertex)
                self.__apply_scaling_factor(point)
                self.__move_to_screen_center(point)
                points.append(point)
            self.__draw_polygon(points, screen, polygon.color)

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

    def __draw_polygon(self, points: list[np.ndarray], screen: Surface, color: tuple[int, int, int]) -> None:
        if len(points) < 2:
            return
        
        line_width = 1
        if self.occlussion_enabled:
            line_width = 0

        pygame.draw.polygon(screen, color, points, line_width)

    def __compare_polygons_occlusion(self, Q: Polygon, P: Polygon) -> int:
        if not self.__do_rects_intersect(Q.get_bounding_rectangle(), P.get_bounding_rectangle()):
            return 0
        
        camera_position = Vertex(0, 0, 0)

        is_p_on_the_other_side = True
        q_plane = Q.get_plane()
        camera_side = np.dot(q_plane, camera_position.to_vector())
        for vertex in P.vertices:
            vertex_side = np.dot(q_plane, vertex.to_vector())
            if vertex_side * camera_side > 0:
                is_p_on_the_other_side = False
                break
        if is_p_on_the_other_side:
            return 1

        is_q_on_the_other_side = True
        p_plane = P.get_plane()
        camera_side = np.dot(p_plane, camera_position.to_vector())
        for vertex in Q.vertices:
            vertex_side = np.dot(p_plane, vertex.to_vector())
            if vertex_side * camera_side > 0:
                is_q_on_the_other_side = False
                break
        if is_q_on_the_other_side:
            return -1

        return 0

    def __do_rects_intersect(self, rect1: Rect, rect2: Rect) -> bool:
        return not (rect1.right < rect2.left or
                    rect1.left > rect2.right or
                    rect1.bottom < rect2.top or
                    rect1.top > rect2.bottom)
