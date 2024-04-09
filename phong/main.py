import pygame
from sphere_camera import SphereCamera
from keyboard_handler import KeyboardHandler
from example_materials import metal_material

BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 800
FPS = 60
SPHERE_RADIUS = 200

def main():
    pygame.display.set_caption("Grafika komputerowa - projekt")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen_center = (WIDTH // 2, HEIGHT // 2)

    camera = SphereCamera(screen_center, metal_material)
    keyboard_handler = KeyboardHandler(camera)
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        keyboard_handler.handle_keyboard_events()
        screen.fill(BLACK)
        camera.draw_sphere(screen, SPHERE_RADIUS)
        pygame.display.update()

if __name__ == "__main__":
    main()
