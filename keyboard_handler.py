import pygame
from camera import Camera

class KeyboardHandler:
    def __init__(self, camera: Camera) -> None:
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
                if event.key == pygame.K_UP:
                    self.camera.move_up()
                if event.key == pygame.K_DOWN:
                    self.camera.move_down()
                if event.key == pygame.K_LEFT:
                    self.camera.move_left()
                if event.key == pygame.K_RIGHT:
                    self.camera.move_right()
                if event.key == pygame.K_z:
                    self.camera.move_forward()
                if event.key == pygame.K_x:
                    self.camera.move_backward()
                if event.key == pygame.K_w:
                    self.camera.rotate_x_positive()
                if event.key == pygame.K_s:
                    self.camera.rotate_x_negative()
                if event.key == pygame.K_a:
                    self.camera.rotate_y_positive()
                if event.key == pygame.K_d:
                    self.camera.rotate_y_negative()
                if event.key == pygame.K_q:
                    self.camera.rotate_z_positive()
                if event.key == pygame.K_e:
                    self.camera.rotate_z_negative()
