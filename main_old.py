import pygame
import numpy as np
from math import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 800

pygame.display.set_caption("Grafika komputerowa - projekt")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100
screen_middle = [WIDTH/2, HEIGHT/2]

points = []

points.append(np.array([-1, -1, 1, 1]))
points.append(np.array([1, -1, 1, 1]))
points.append(np.array([1,  1, 1, 1]))
points.append(np.array([-1, 1, 1, 1]))
points.append(np.array([-1, -1, -1, 1]))
points.append(np.array([1, -1, -1, 1]))
points.append(np.array([1, 1, -1, 1]))
points.append(np.array([-1, 1, -1, 1]))

projected_points = [
    [n, n] for n in range(len(points))
]

def create_projection_matrix(aspect_ratio, fov, near, far):
    return np.array([
        [1 / (aspect_ratio * tan(fov / 2)), 0, 0, 0],
        [0, 1 / tan(fov / 2), 0, 0],
        [0, 0, - (far + near) / (far - near), (-2 * far * near) / (far - near)],
        [0, 0, -1, 0]
    ])

def connect_points(i, j, points):
    pygame.draw.line(screen, WHITE, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

def rotate_x(angle, points):
    rotation_matrix = np.array([
        [1, 0, 0, 0],
        [0, cos(angle), -sin(angle), 0],
        [0, sin(angle), cos(angle), 0],
        [0, 0, 0, 1]
    ])
    return [np.dot(rotation_matrix, point) for point in points]

def rotate_y(angle, points):
    rotation_matrix = np.array([
        [cos(angle), 0, sin(angle), 0],
        [0, 1, 0, 0],
        [-sin(angle), 0, cos(angle), 0],
        [0, 0, 0, 1]
    ])
    return [np.dot(rotation_matrix, point) for point in points]

def rotate_z(angle, points):
    rotation_matrix = np.array([
        [cos(angle), -sin(angle), 0, 0],
        [sin(angle), cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return [np.dot(rotation_matrix, point) for point in points]

def clip_points(points, near, far):
    return points
    clipped_points = []
    for point in points:
        z = point[2]
        if near < z < far:
            clipped_points.append(point)
    return clipped_points

aspect_ratio = WIDTH / HEIGHT
fov = radians(45)
near = 0.01
far = 1000

projection_matrix = create_projection_matrix(aspect_ratio, fov, near, far)

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
            # Update translation matrix based on key events
            translation = np.zeros(4)
            if event.key == pygame.K_UP:
                translation[1] += 0.1
            elif event.key == pygame.K_DOWN:
                translation[1] -= 0.1
            elif event.key == pygame.K_LEFT:
                translation[0] += 0.1
            elif event.key == pygame.K_RIGHT:
                translation[0] -= 0.1
            elif event.key == pygame.K_z:
                translation[2] += 0.1
            elif event.key == pygame.K_x:
                translation[2] -= 0.1
            # Update rotation matrix based on key events
            if event.key == pygame.K_w:
                points = rotate_x(radians(5), points)
            elif event.key == pygame.K_s:
                points = rotate_x(radians(-5), points)
            elif event.key == pygame.K_a:
                points = rotate_y(radians(5), points)
            elif event.key == pygame.K_d:
                points = rotate_y(radians(-5), points)
            elif event.key == pygame.K_q:
                points = rotate_z(radians(5), points)
            elif event.key == pygame.K_e:
                points = rotate_z(radians(-5), points)
            # Apply translation to each point in the scene
            points = [point + translation for point in points]

    screen.fill(BLACK)

    clipped_points = clip_points(points, near, far)

    for index, point in enumerate(clipped_points):
        projected2d = np.dot(projection_matrix, point.reshape((4, 1)))
        
        # Perspective division
        x = int(projected2d[0][0] / projected2d[2][0] * scale) + screen_middle[0]
        y = int(projected2d[1][0] / projected2d[2][0] * scale) + screen_middle[1]

        projected_points[index] = [x, y]

    print(projected_points)
    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)

    pygame.display.update()
