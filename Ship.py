import pygame
import random
import os
import math

# Ship settings
ship_image = pygame.image.load('Parker_EW200_AY2025.pygame/Tiles/PNG/playerShip3_green.png') 
ship_image = pygame.transform.scale(ship_image, (50, 50))  # Adjust size as needed
ship_rect = ship_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
ship_angle = 0  # Initial angle of the ship
speed = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  # Move forward
        ship_rect.x += speed * math.cos(math.radians(ship_angle))
        ship_rect.y += speed * math.sin(math.radians(ship_angle))
    if keys[pygame.K_s]:  # Move backward
        ship_rect.x -= speed * math.cos(math.radians(ship_angle))
        ship_rect.y -= speed * math.sin(math.radians(ship_angle))
    if keys[pygame.K_a]:  # Rotate left
        ship_angle += 5
    if keys[pygame.K_d]:  # Rotate right
        ship_angle -= 5

    # Clear the screen
    screen.blit(background_image, (0, 0))

    # Draw meteors
    for meteor in meteors:
        screen.blit(meteor[0], (meteor[1], meteor[2]))

    # Rotate and draw the ship
    rotated_ship = pygame.transform.rotate(ship_image, ship_angle)
    new_rect = rotated_ship.get_rect(center=ship_rect.center)
    screen.blit(rotated_ship, new_rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()