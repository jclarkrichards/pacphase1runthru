import pygame
from vectors import Vector2D
from constants import *

class Text(object):
    def __init__(self, name, text, x, y):
        self.name = name
        self.text = text
        self.position = Vector2D(x, y)

    def render(self, screen):
        screen.blit(self.text, self.position.toTuple())


class TextGroup(object):
    def __init__(self):
        self.words = []
        pygame.font.init()
        self.font_path = "PressStart2P.ttf"
        self.font_size = WIDTH
        self.font = pygame.font.Font(self.font_path, self.font_size)

    def add(self, name, text, x=0, y=0, align="", size=1.0, color=WHITE):
        if size != 1.0:
            font = pygame.font.Font(self.font_path, 
                                    int(self.font_size*size))
        else:
            font = self.font

        if align == "left":
            x = 0
        elif align == "center":
            x = (SCREENSIZE[0] - (self.font_size*size * len(str(text)))) / 2
        elif align == "right":
            x = SCREENSIZE[0] - (self.font_size*size * len(str(text)))

        label = font.render(str(text), 1, color)
        self.words.append(Text(name, label, x, y))

    def remove(self, name):
        word = self.findWord(name)
        if word is not None:
            self.words.remove(word)

    def findWord(self, name):
        for word in self.words:
            if word.name == str(name):
                return word
        return None

    def render(self, screen):
        for word in self.words:
            word.render(screen)

    


