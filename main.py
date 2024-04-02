import pygame
from math import radians
from file_reader import FileReader
from camera import Camera

BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 800

pygame.display.set_caption("Grafika komputerowa - projekt")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fov = radians(45)
near = 0.01
far = 1000

file_reader = FileReader("cube.txt")
lines = file_reader.read()
camera = Camera(lines, fov, near, far, WIDTH, HEIGHT)
clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    screen.fill(BLACK)
    camera.draw_scene(screen)
    pygame.display.update()
