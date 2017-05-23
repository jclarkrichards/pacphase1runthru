import pygame
from constants import *

class Lives(object):
    def __init__(self, spritesheet):
        #self.image = pygame.image.load("Images/pacman.png").convert()
        self.width, self.height = 32, 32
        self.image = spritesheet.getImage(1, 0, self.width, self.height)
        #self.image.set_colorkey(TRANSPARENT)
        #self.width, self.height = self.image.get_size()
        self.gap = 10

    def render(self, screen, num):
        for i in range(num):
            x = self.gap + (self.width + self.gap) * i
            y = HEIGHT * NROWS - self.height
            screen.blit(self.image, (x, y))
