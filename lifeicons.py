import pygame
from constants import *

class Lives(object):
    def __init__(self):
        self.image = pygame.image.load("Images/pacman.png").convert()
        self.image.set_colorkey(TRANSPARENT)
        self.width, self.height = self.image.get_size()
        self.gap = 10

    def render(self, screen, num):
        for i in range(num):
            x = self.gap + (self.width + self.gap) * i
            y = HEIGHT * NROWS - self.height
            screen.blit(self.image, (x, y))
