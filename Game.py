import pygame

HEIGHT = 600
WIDTH = 900
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# Background
background_image = pygame.image.load('Tiles\Backgrounds\darkPurple.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  

# Astroids





while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))

    pygame.display.flip()
    clock.tick(60)  

pygame.quit()