import pygame
from math import radians
from file_reader import FileReader
from camera import Camera
from keyboard_handler import KeyboardHandler

BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 800
FPS = 60

def main():
    pygame.display.set_caption("Grafika komputerowa - projekt")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fov = radians(45)
    near = 0.01
    far = 1000

    file_reader = FileReader("scene.txt")
    polygons = file_reader.read()
    camera = Camera(polygons, fov, near, far, WIDTH, HEIGHT)
    keyboard_handler = KeyboardHandler(camera)
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        keyboard_handler.handle_keyboard_events()
        screen.fill(BLACK)
        camera.draw_scene(screen)
        pygame.display.update()

if __name__ == "__main__":
    main()
