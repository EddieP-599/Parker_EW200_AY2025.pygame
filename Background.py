import pygame
import random
import os

HEIGHT = 600
WIDTH = 1000

background_image = pygame.image.load('Tiles\Backgrounds\darkPurple.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  