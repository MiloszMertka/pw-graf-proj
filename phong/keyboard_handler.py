import pygame
from sphere_camera import SphereCamera
from example_materials import metal_material, chalk_material, plastic_material, wood_material

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.camera.move_light_forward()
                if event.key == pygame.K_s:
                    self.camera.move_light_backward()
                if event.key == pygame.K_a:
                    self.camera.move_light_left()
                if event.key == pygame.K_d:
                    self.camera.move_light_right()
                if event.key == pygame.K_q:
                    self.camera.move_light_up()
                if event.key == pygame.K_e:
                    self.camera.move_light_down()
                if event.key == pygame.K_r:
                    self.camera.reset_light_position()
                if event.key == pygame.K_1:
                    self.camera.material = metal_material
                if event.key == pygame.K_2:
                    self.camera.material = wood_material
                if event.key == pygame.K_3:
                    self.camera.material = plastic_material
                if event.key == pygame.K_4:
                    self.camera.material = chalk_material