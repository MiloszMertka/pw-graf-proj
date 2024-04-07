import pygame
from sphere_camera import SphereCamera

class KeyboardHandler:
    def __init__(self, camera: SphereCamera) -> None:
        self.camera = camera

    def handle_keyboard_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
