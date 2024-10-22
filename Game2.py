import pygame
import random
import os

HEIGHT = 600
WIDTH = 1000
NUM_METEORS = 10  
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

background_image = pygame.image.load('Tiles\Backgrounds\darkPurple.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  

# Load meteor images
meteor_images = []
meteor_dir = 'Tiles\PNG\Meteors' 

for filename in os.listdir(meteor_dir):
    if filename.endswith('.png'):
        meteor_images.append(pygame.image.load(os.path.join(meteor_dir, filename)))


meteors = []
for _ in range(NUM_METEORS):
    image = random.choice(meteor_images)
    size = random.randint(20, 150)  # Random size factor
    scaled_image = pygame.transform.scale(image, (size, size))
    x = random.randint(0, WIDTH - size)
    y = random.randint(0, HEIGHT - size)
    meteors.append((scaled_image, x, y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))

    for meteor in meteors:
        screen.blit(meteor[0], (meteor[1], meteor[2])) 

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()