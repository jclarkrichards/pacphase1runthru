import pygame
from vectors import Vector2D
from constants import *

class Lives(object):
    def __init__(self):
        self.image = pygame.image.load("Images/pacman.png").convert()
        self.image.set_colorkey(WHITE)
        self.width, self.height = self.image.get_size()
        #self.width = self.image.get_rect()[2]
        #self.height = self.image.get_rect()[3]
        self.gap = 10
        #print type(self.image)

    def render(self, screen, num):
        for i in range(num):
            x = self.gap + (self.width + self.gap) * i
            y = HEIGHT * NROWS - self.height
            #y = HEIGHT * (NROWS - 2)
            screen.blit(self.image, (x, y))
