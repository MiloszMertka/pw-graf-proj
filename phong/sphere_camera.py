from math import sin, cos, radians, sqrt
import pygame
from pygame import Surface
from material import Material

LIGHT_MOVE_STEP = 0.1
DEFAULT_LIGHT_POSITION = (0.75, 0.5, 0.5)

class SphereCamera:
    def __init__(self, screen_center: tuple[int, int], material: Material) -> None:
        self.screen_center = screen_center
        self.light_position = DEFAULT_LIGHT_POSITION
        self.material = material

    def move_light_up(self) -> None:
        self.light_position = (self.light_position[0], self.light_position[1] + LIGHT_MOVE_STEP, self.light_position[2])

    def move_light_down(self) -> None:
        self.light_position = (self.light_position[0], self.light_position[1] - LIGHT_MOVE_STEP, self.light_position[2])

    def move_light_left(self) -> None:
        self.light_position = (self.light_position[0] + LIGHT_MOVE_STEP, self.light_position[1], self.light_position[2])

    def move_light_right(self) -> None:
        self.light_position = (self.light_position[0] - LIGHT_MOVE_STEP, self.light_position[1], self.light_position[2])

    def move_light_forward(self) -> None:
        self.light_position = (self.light_position[0], self.light_position[1], self.light_position[2] - LIGHT_MOVE_STEP)

    def move_light_backward(self) -> None:
        self.light_position = (self.light_position[0], self.light_position[1], self.light_position[2] + LIGHT_MOVE_STEP)

    def reset_light_position(self) -> None:
        self.light_position = DEFAULT_LIGHT_POSITION

    def draw_sphere(self, screen: Surface, radius: float) -> None:
        for i in range(360):
            for j in range(180):
                theta1 = radians(i)
                theta2 = radians(i + 1)
                phi1 = radians(j)
                phi2 = radians(j + 1)

                x1, y1, z1 = self.__convert_to_cartesian_coordinates(radius, theta1, phi1)
                x2, y2, z2 = self.__convert_to_cartesian_coordinates(radius, theta2, phi1)
                x3, y3, z3 = self.__convert_to_cartesian_coordinates(radius, theta1, phi2)
                x4, y4, z4 = self.__convert_to_cartesian_coordinates(radius, theta2, phi2)

                normal = self.__calculate_normal_vector((x1, y1, z1), (x2, y2, z2), (x3, y3, z3))
                intensity = self.__calculate_intensity(normal)

                red, green, blue = self.material.color
                color = (int(red * intensity),
                         int(green * intensity),
                         int(blue * intensity))

                x1, y1 = self.__move_to_screen_center((x1, y1))
                x2, y2 = self.__move_to_screen_center((x2, y2))
                x3, y3 = self.__move_to_screen_center((x3, y3))
                x4, y4 = self.__move_to_screen_center((x4, y4))

                pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x4, y4), (x3, y3)])

    def __convert_to_cartesian_coordinates(self, radius: float, theta: float, phi: float) -> tuple[float, float, float]:
        x = radius * sin(phi) * cos(theta)
        y = radius * sin(phi) * sin(theta)
        z = radius * cos(phi)
        return x, y, z
    
    def __move_to_screen_center(self, point: tuple[float, float]) -> tuple[float, float]:
        x, y = point
        x += self.screen_center[0]
        y += self.screen_center[1]
        return x, y
    
    def __calculate_normal_vector(self, v1: tuple[float, float, float], v2: tuple[float, float, float], v3: tuple[float, float, float]) -> tuple[float, float, float]:
        x1, y1, z1 = v1
        x2, y2, z2 = v2
        x3, y3, z3 = v3

        a = (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)
        b = (z2 - z1) * (x3 - x1) - (x2 - x1) * (z3 - z1)
        c = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

        length = sqrt(a ** 2 + b ** 2 + c ** 2)

        if length == 0:
            return 0, 0, 0
        else:
            return a / length, b / length, c / length

    def __calculate_intensity(self, normal: tuple[float, float, float]) -> float:
        diffuse = max(0, normal[0] * self.light_position[0] +
                      normal[1] * self.light_position[1] +
                      normal[2] * self.light_position[2]) * self.material.diffuse

        reflection = 2 * (normal[0] * self.light_position[0] +
                          normal[1] * self.light_position[1] +
                          normal[2] * self.light_position[2])
        reflected_light = (-self.light_position[0] + reflection * normal[0],
                           -self.light_position[1] + reflection * normal[1],
                           -self.light_position[2] + reflection * normal[2])

        specular = max(0, reflected_light[0] * 0 +
                       reflected_light[1] * 0 +
                       reflected_light[2] * 1) ** self.material.shininess * self.material.specular

        return min(1, self.material.ambient + diffuse + specular)
