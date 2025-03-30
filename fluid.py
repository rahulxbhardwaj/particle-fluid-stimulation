import pygame
import socket
import sys
import random
import numpy as np
import math
from numba import njit, prange

# Initialize Pygame and fullscreen
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("High-Performance Fluid Simulation - Fullscreen RGB")
clock = pygame.time.Clock()

# Particle settings
PARTICLE_COUNT = 3000
PARTICLE_RADIUS = 9
BG_COLOR = (0, 0, 0)

# UDP Settings
UDP_IP = "0.0.0.0"
UDP_PORT = 4210
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

# Particle array: x, y, vx, vy
particles = np.zeros((PARTICLE_COUNT, 4), dtype=np.float32)
particles[:, 0] = np.random.uniform(0, WIDTH, PARTICLE_COUNT)
particles[:, 1] = np.random.uniform(0, HEIGHT, PARTICLE_COUNT)
particles[:, 2] = np.random.uniform(-1, 1, PARTICLE_COUNT)
particles[:, 3] = np.random.uniform(-1, 1, PARTICLE_COUNT)

ax, ay = 0.0, 0.0

@njit(parallel=True, fastmath=True)
def update_particles(particles, ax, ay, width, height, radius):
    for i in prange(particles.shape[0]):
        p = particles[i]
        p[2] += ax * 0.8
        p[3] += ay * 0.8
        p[2] *= 0.99
        p[3] *= 0.99
        p[0] += p[2]
        p[1] += p[3]

        # Boundary collision
        if p[0] < radius:
            p[0] = radius
            p[2] *= -0.5
        if p[0] > width - radius:
            p[0] = width - radius
            p[2] *= -0.5
        if p[1] < radius:
            p[1] = radius
            p[3] *= -0.5
        if p[1] > height - radius:
            p[1] = height - radius
            p[3] *= -0.5

@njit(parallel=True, fastmath=True)
def resolve_collisions(particles, radius):
    min_dist_sq = (radius * 2) ** 2
    for i in prange(particles.shape[0]):
        for j in range(i + 1, particles.shape[0]):
            dx = particles[i, 0] - particles[j, 0]
            dy = particles[i, 1] - particles[j, 1]
            dist_sq = dx * dx + dy * dy
            if dist_sq < min_dist_sq and dist_sq > 0:
                dist = math.sqrt(dist_sq)
                overlap = (2 * radius - dist) * 0.5
                nx, ny = dx / dist, dy / dist
                particles[i, 0] += nx * overlap
                particles[i, 1] += ny * overlap
                particles[j, 0] -= nx * overlap
                particles[j, 1] -= ny * overlap

running = True
while running:
    clock.tick(60)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Sensor data receive
    try:
        data, _ = sock.recvfrom(1024)
        decoded = data.decode().strip()
        accel_data = list(map(float, decoded.split(',')))
        ax = accel_data[0] / 10
        ay = accel_data[1] / 10
    except:
        pass

    # Update and collision
    update_particles(particles, ax, ay, WIDTH, HEIGHT, PARTICLE_RADIUS)
    resolve_collisions(particles, PARTICLE_RADIUS)

    # Draw particles with RGB gradient effect
    for i in range(PARTICLE_COUNT):
        color = pygame.Color(0)
        color.hsva = (i / PARTICLE_COUNT * 360, 100, 100, 100)  # Hue shifts across particles
        pygame.draw.circle(screen, color,
                           (int(particles[i, 0]), int(particles[i, 1])),
                           PARTICLE_RADIUS)

    pygame.display.flip()

pygame.quit()
sys.exit()
