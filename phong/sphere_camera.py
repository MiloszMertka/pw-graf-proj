from math import sin, cos, radians
import pygame
from pygame import Surface

class SphereCamera:
    def __init__(self, screen_center: tuple[int, int]) -> None:
        self.screen_center = screen_center

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

                x1, y1 = self.__move_to_screen_center((x1, y1))
                x2, y2 = self.__move_to_screen_center((x2, y2))
                x3, y3 = self.__move_to_screen_center((x3, y3))
                x4, y4 = self.__move_to_screen_center((x4, y4))

                pygame.draw.polygon(screen, (255, 255, 255), [(x1, y1), (x2, y2), (x4, y4), (x3, y3)])

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
