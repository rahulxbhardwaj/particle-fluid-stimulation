import pygame
import socket
import sys
import random
import time

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Fluid Rush - Challenge Mode")
clock = pygame.time.Clock()

# UDP Sensor Setup
UDP_IP = "0.0.0.0"
UDP_PORT = 4210
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

# Ball properties
BALL_RADIUS = 40
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
vx, vy = 0, 0

# Target Box
BOX_SIZE = 200
box_x, box_y = random.randint(0, WIDTH - BOX_SIZE), random.randint(0, HEIGHT - BOX_SIZE)
box_color = (255, 0, 0)

# Game variables
score = 0
hold_time = 3  # seconds required inside the box
inside_box_timer = 0
ax, ay = 0, 0
font = pygame.font.SysFont("Arial", 40)

running = True
while running:
    clock.tick(60)
    screen.fill((20, 20, 30))

    # Handle exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Receive sensor data
    try:
        data, _ = sock.recvfrom(1024)
        decoded = data.decode().strip()
        accel_data = list(map(float, decoded.split(',')))
        ax = accel_data[0] / 5   # Tune sensitivity
        ay = accel_data[1] / 5
    except:
        pass

    # Update ball physics
    vx += ax
    vy += ay
    vx *= 0.98  # Damping
    vy *= 0.98
    ball_x += vx
    ball_y += vy

    # Boundary check
    if ball_x < BALL_RADIUS: ball_x, vx = BALL_RADIUS, -vx * 0.5
    if ball_x > WIDTH - BALL_RADIUS: ball_x, vx = WIDTH - BALL_RADIUS, -vx * 0.5
    if ball_y < BALL_RADIUS: ball_y, vy = BALL_RADIUS, -vy * 0.5
    if ball_y > HEIGHT - BALL_RADIUS: ball_y, vy = HEIGHT - BALL_RADIUS, -vy * 0.5

    # Draw target box
    pygame.draw.rect(screen, box_color, (box_x, box_y, BOX_SIZE, BOX_SIZE), 5)

    # Check if ball is inside the target box
    if box_x < ball_x < box_x + BOX_SIZE and box_y < ball_y < box_y + BOX_SIZE:
        inside_box_timer += clock.get_time() / 1000  # Time inside the box
        progress = min(inside_box_timer / hold_time, 1)
        pygame.draw.rect(screen, (0, 255, 0), (box_x, box_y + BOX_SIZE + 10, BOX_SIZE * progress, 10))
    else:
        inside_box_timer = 0  # Reset if ball leaves the box

    # If held long enough, score and spawn next box
    if inside_box_timer >= hold_time:
        score += 1
        box_x, box_y = random.randint(0, WIDTH - BOX_SIZE), random.randint(0, HEIGHT - BOX_SIZE)
        inside_box_timer = 0

    # Draw ball
    pygame.draw.circle(screen, (0, 200, 255), (int(ball_x), int(ball_y)), BALL_RADIUS)

    # Display Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (50, 50))

    # Instructions
    instruction = font.render("Keep the ball in the box for 3 sec!", True, (200, 200, 200))
    screen.blit(instruction, (50, HEIGHT - 80))

    pygame.display.flip()

pygame.quit()
sys.exit()
