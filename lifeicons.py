import pygame
from constants import *

class Lives(object):
    def __init__(self):
        self.image = pygame.image.load("Images/pacmanTest.png").convert()
        self.image.set_colorkey((255,0,255))
        self.width, self.height = self.image.get_size()
        self.gap = 10

    def render(self, screen, num):
        for i in range(num):
            x = self.gap + (self.width + self.gap) * i
            y = HEIGHT * NROWS - self.height
            screen.blit(self.image, (x, y))
