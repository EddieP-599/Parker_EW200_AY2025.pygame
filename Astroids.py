import pygame
import random
import os

meteor_images = []
meteor_dir = 'Tiles\PNG\Meteors' 
NUM_METEORS = 20
HEIGHT = 600
WIDTH = 1000

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