import pygame
import random
import os
import math

# Constants
HEIGHT = 600
WIDTH = 1000
NUM_METEORS = 10
MIN_DISTANCE = 100  # Minimum distance between centers of meteors
BULLET_SPEED = 10

# Load images
meteor_images = []
meteor_dir = 'Parker_EW200_AY2025.pygame/Tiles/PNG/Meteors'

background_image = pygame.image.load('Parker_EW200_AY2025.pygame/Tiles/Backgrounds/darkPurple.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load meteor images
for filename in os.listdir(meteor_dir):
    if filename.endswith('.png'):
        meteor_images.append(pygame.image.load(os.path.join(meteor_dir, filename)))

# Bullet class
class Bullet:
    def __init__(self, x, y, angle, image, owner):
        self.x = x
        self.y = y
        self.angle = angle
        self.image = pygame.transform.rotate(image, 90)  # Rotate the image 90 degrees
        self.owner = owner  # Track which player owns the bullet

    def update(self):
        # Update bullet position based on angle and speed
        self.x += BULLET_SPEED * math.cos(math.radians(self.angle))
        self.y -= BULLET_SPEED * math.sin(math.radians(self.angle))

    def draw(self, surface):
        # Rotate and draw the bullet on the screen
        rotated_image = pygame.transform.rotate(self.image, self.angle - 90)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, rect.topleft)

# Load bullet images
laser_blue_image = pygame.image.load('Parker_EW200_AY2025.pygame/Tiles/PNG/Lasers/laserBlue02.png')
laser_green_image = pygame.image.load('Parker_EW200_AY2025.pygame/Tiles/PNG/Lasers/laserGreen04.png')

# Load hit image
hit_image = pygame.image.load('Parker_EW200_AY2025.pygame/Tiles/PNG/UI/numeralX.png')
hit_image = pygame.transform.scale(hit_image, (25, 25))  # Adjust size as needed

# Resize bullet images
laser_blue_image = pygame.transform.scale(laser_blue_image, (10, 5))  # Adjust size as needed
laser_green_image = pygame.transform.scale(laser_green_image, (10, 5))  # Adjust size as needed

# Function to check for distance between centers
def is_too_close(new_position, meteors, min_distance):
    new_x, new_y = new_position
    for _, x, y in meteors:
        if math.hypot(new_x - x, new_y - y) < min_distance:
            return True
    return False

# Function to check if the meteor overlaps with any ship
def is_overlapping_with_ships(new_rect, player1_rect, player2_rect):
    return new_rect.colliderect(player1_rect) or new_rect.colliderect(player2_rect)

# Function to check bullet collision with meteors
def check_bullet_collision(bullets, meteors):
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet.x, bullet.y, 10, 5)  # Assuming bullets are 10x5
        for meteor in meteors:
            meteor_rect = meteor[0].get_rect(topleft=(meteor[1], meteor[2]))
            if bullet_rect.colliderect(meteor_rect):
                bullets.remove(bullet)
                break

# Load ship images
player1_image = pygame.image.load('Parker_EW200_AY2025.pygame/Tiles/PNG/playerShip3_green.png')
player2_image = pygame.image.load('Parker_EW200_AY2025.pygame/Tiles/PNG/playerShip3_blue.png')

# Resize the images
player1_image = pygame.transform.scale(player1_image, (25, 25))  # Adjust size as needed
player2_image = pygame.transform.scale(player2_image, (25, 25))  # Adjust size as needed

# Initialize global variables
player1_rect = None
player2_rect = None

# Reset the game state
def reset_game():
    global player1_rect, player2_rect, player1_angle, player2_angle
    global player1_alive, player2_alive, meteors, bullets

    # Reset player 1 state
    player1_rect = player1_image.get_rect(topleft=(0, 0))
    player1_angle = 315  # Initial angle of player 1's ship
    player1_alive = True  # Track if player 1 is alive

    # Reset player 2 state
    player2_rect = player2_image.get_rect(topleft=(WIDTH - 25, HEIGHT - 25))  # Start at bottom right
    player2_angle = 135  # Initial angle of player 2's ship
    player2_alive = True  # Track if player 2 is alive

    # Generate meteors
    meteors = []
    for _ in range(NUM_METEORS):
        image = random.choice(meteor_images)
        size = random.randint(20, 100)  # Random size factor
        scaled_image = pygame.transform.scale(image, (size, size))

        # Find a position that doesn't overlap and respects the minimum distance
        while True:
            x = random.randint(0, WIDTH - size)
            y = random.randint(0, HEIGHT - size)
            center_position = (x + size // 2, y + size // 2)  # Calculate center of the meteor
            meteor_rect = scaled_image.get_rect(topleft=(x, y))

            if (not is_too_close(center_position, meteors, MIN_DISTANCE) and 
                    not is_overlapping_with_ships(meteor_rect, player1_rect, player2_rect)):
                meteors.append((scaled_image, x, y))
                break

    # Reset bullets
    bullets = []

# Initialize game state
reset_game()

# List to hold bullets
bullets = []
# Track if the shoot keys are pressed
player1_can_shoot = True
player2_can_shoot = True

# Game over state
game_over = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # Player 1 controls (W/S for movement)
        if keys[pygame.K_w] and player1_alive:  # Move forward
            new_x = player1_rect.x + 3 * math.cos(math.radians(player1_angle))
            new_y = player1_rect.y - 3 * math.sin(math.radians(player1_angle))
            new_rect = player1_rect.move(new_x - player1_rect.x, new_y - player1_rect.y)

            can_move = True
            for meteor in meteors:
                meteor_rect = meteor[0].get_rect(topleft=(meteor[1], meteor[2]))
                if new_rect.colliderect(meteor_rect):
                    can_move = False
                    break
            if can_move and 0 <= new_x <= WIDTH - player1_rect.width and 0 <= new_y <= HEIGHT - player1_rect.height:
                player1_rect.topleft = (new_x, new_y)

        if keys[pygame.K_s] and player1_alive:  # Move backward
            new_x = player1_rect.x - 3 * math.cos(math.radians(player1_angle))
            new_y = player1_rect.y + 3 * math.sin(math.radians(player1_angle))
            new_rect = player1_rect.move(new_x - player1_rect.x, new_y - player1_rect.y)

            can_move = True
            for meteor in meteors:
                meteor_rect = meteor[0].get_rect(topleft=(meteor[1], meteor[2]))
                if new_rect.colliderect(meteor_rect):
                    can_move = False
                    break
            if can_move and 0 <= new_x <= WIDTH - player1_rect.width and 0 <= new_y <= HEIGHT - player1_rect.height:
                player1_rect.topleft = (new_x, new_y)

        if keys[pygame.K_a] and player1_alive:  # Rotate left
            player1_angle += 5
        if keys[pygame.K_d] and player1_alive:  # Rotate right
            player1_angle -= 5

        # Player 2 controls (Arrow keys for movement)
        if keys[pygame.K_UP] and player2_alive:  # Move forward
            new_x = player2_rect.x + 3 * math.cos(math.radians(player2_angle))
            new_y = player2_rect.y - 3 * math.sin(math.radians(player2_angle))
            new_rect = player2_rect.move(new_x - player2_rect.x, new_y - player2_rect.y)

            can_move = True
            for meteor in meteors:
                meteor_rect = meteor[0].get_rect(topleft=(meteor[1], meteor[2]))
                if new_rect.colliderect(meteor_rect):
                    can_move = False
                    break
            if can_move and 0 <= new_x <= WIDTH - player2_rect.width and 0 <= new_y <= HEIGHT - player2_rect.height:
                player2_rect.topleft = (new_x, new_y)

        if keys[pygame.K_DOWN] and player2_alive:  # Move backward
            new_x = player2_rect.x - 3 * math.cos(math.radians(player2_angle))
            new_y = player2_rect.y + 3 * math.sin(math.radians(player2_angle))
            new_rect = player2_rect.move(new_x - player2_rect.x, new_y - player2_rect.y)

            can_move = True
            for meteor in meteors:
                meteor_rect = meteor[0].get_rect(topleft=(meteor[1], meteor[2]))
                if new_rect.colliderect(meteor_rect):
                    can_move = False
                    break
            if can_move and 0 <= new_x <= WIDTH - player2_rect.width and 0 <= new_y <= HEIGHT - player2_rect.height:
                player2_rect.topleft = (new_x, new_y)

        if keys[pygame.K_LEFT] and player2_alive:  # Rotate left
            player2_angle += 5
        if keys[pygame.K_RIGHT] and player2_alive:  # Rotate right
            player2_angle -= 5

        # Shooting
        if keys[pygame.K_q] and player1_can_shoot and player1_alive:  # Ship 1 shoots with 'Q'
            bullets.append(Bullet(player1_rect.centerx, player1_rect.centery, player1_angle, laser_green_image, owner=1))
            player1_can_shoot = False  # Prevent further shots until the key is released

        if keys[pygame.K_SPACE] and player2_can_shoot and player2_alive:  # Ship 2 shoots with space bar
            bullets.append(Bullet(player2_rect.centerx, player2_rect.centery, player2_angle, laser_blue_image, owner=2))
            player2_can_shoot = False  # Prevent further shots until the key is released

        # Allow shooting again when the keys are released
        if not keys[pygame.K_q]:
            player1_can_shoot = True
        if not keys[pygame.K_SPACE]:
            player2_can_shoot = True

        # Update and draw bullets
        for bullet in bullets[:]:
            bullet.update()
            if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
                bullets.remove(bullet)

        # Check bullet collisions with meteors
        check_bullet_collision(bullets, meteors)

        # Check for collisions with players, but only check for opposing bullets
        for bullet in bullets[:]:
            if player1_alive and bullet.owner == 2 and player1_rect.collidepoint((bullet.x, bullet.y)):
                player1_alive = False
                bullets.remove(bullet)
                game_over = True  # Set game over when player 1 is hit
            if player2_alive and bullet.owner == 1 and player2_rect.collidepoint((bullet.x, bullet.y)):
                player2_alive = False
                bullets.remove(bullet)
                game_over = True  # Set game over when player 2 is hit

    else:
        # Wait for Enter key to reset the game
        if keys[pygame.K_RETURN]:
            reset_game()
            game_over = False

    # Clear the screen
    screen.blit(background_image, (0, 0))

    # Draw meteors
    for meteor in meteors:
        screen.blit(meteor[0], (meteor[1], meteor[2]))

    # Rotate and draw player 1's ship or hit image
    if player1_alive:
        rotated_ship1 = pygame.transform.rotate(player1_image, player1_angle - 90)
        new_rect1 = rotated_ship1.get_rect(center=player1_rect.center)
        screen.blit(rotated_ship1, new_rect1.topleft)
    else:
        screen.blit(hit_image, player1_rect.topleft)  # Draw the hit image

    # Rotate and draw player 2's ship or hit image
    if player2_alive:
        rotated_ship2 = pygame.transform.rotate(player2_image, player2_angle - 90)
        new_rect2 = rotated_ship2.get_rect(center=player2_rect.center)
        screen.blit(rotated_ship2, new_rect2.topleft)
    else:
        screen.blit(hit_image, player2_rect.topleft)  # Draw the hit image

    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()