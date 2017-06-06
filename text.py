import pygame
from vectors import Vector2D
from constants import *

class Digit(object):
    def __init__(self, image, x, y, size=1.0):
        self.image = image
        self.position = Vector2D(x, y)
            
        if self.image is not None:
            width, height = self.image.get_size()
            if size != 1.0:
                w, h = int(width*size), int(height*size)
                self.image = pygame.transform.scale(self.image, (w, h))

    def render(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.position.toTuple())


class Word(object):
    def __init__(self, name, images, x, y, size=1.0):
        self.name = str(name)
        #self.position = Vector2D(x, y)
        self.images = []
        self.x, self.y = x, y
        for i in range(len(images)):
            self.images.append(Digit(images[i], x + i*16*size, y, size=size))

    def render(self, screen):
        for image in self.images:
            image.render(screen)


class TextGroup(object):
    def __init__(self, sprites):
        self.sprites = sprites
        self.words = []

    def add(self, word, x=0, y=0, align="left", size=1.0):
        images = self.sprites.convert(word)
        if align == "left":
            x = 0
        elif align == "center":
            x = (SCREENSIZE[0] - (WIDTH * len(images))) / 2
        elif align == "right":
            x = SCREENSIZE[0] - (WIDTH * len(images))

        self.words.append(Word(word, images, x, y, size=size))

    def remove(self, name):
        word = self.findWord(name)
        if word is not None:
            self.words.remove(word)

    def update(self, name, newValue, align="left"):
        word = self.findWord(name)
        if word is not None:
            x, y = word.x, word.y
            self.words.remove(word)                
            self.add(name, x=x, y=y, align=align)

    def findWord(self, name):
        for word in self.words:
            if word.name == str(name):
                return word
        return None

    def render(self, screen):
        for word in self.words:
            word.render(screen)

    


class TextSprites(object):
    def __init__(self, spritesheet):
        self.sheet = spritesheet
        self.width, self.height = 16, 16
        self.images = self.getTextImages()
        
    def getTextImages(self):
        images = {}
        images['A'] = self.sheet.getImage(16, 8, self.width, self.height)
        images['B'] = self.sheet.getImage(17, 8, self.width, self.height)
        images['C'] = self.sheet.getImage(18, 8, self.width, self.height)
        images['D'] = self.sheet.getImage(19, 8, self.width, self.height)
        images['E'] = self.sheet.getImage(20, 8, self.width, self.height)
        images['F'] = self.sheet.getImage(21, 8, self.width, self.height)
        images['G'] = self.sheet.getImage(16, 9, self.width, self.height)
        images['H'] = self.sheet.getImage(17, 9, self.width, self.height)
        images['I'] = self.sheet.getImage(18, 9, self.width, self.height)
        images['J'] = self.sheet.getImage(19, 9, self.width, self.height)
        images['K'] = self.sheet.getImage(20, 9, self.width, self.height)
        images['L'] = self.sheet.getImage(21, 9, self.width, self.height)
        images['M'] = self.sheet.getImage(16, 10, self.width, self.height)
        images['N'] = self.sheet.getImage(17, 10, self.width, self.height)
        images['O'] = self.sheet.getImage(18, 10, self.width, self.height)
        images['P'] = self.sheet.getImage(19, 10, self.width, self.height)
        images['Q'] = self.sheet.getImage(20, 10, self.width, self.height)
        images['R'] = self.sheet.getImage(21, 10, self.width, self.height)
        images['S'] = self.sheet.getImage(16, 11, self.width, self.height)
        images['T'] = self.sheet.getImage(17, 11, self.width, self.height)
        images['U'] = self.sheet.getImage(18, 11, self.width, self.height)
        images['V'] = self.sheet.getImage(19, 11, self.width, self.height)
        images['W'] = self.sheet.getImage(20, 11, self.width, self.height)
        images['X'] = self.sheet.getImage(21, 11, self.width, self.height)
        images['Y'] = self.sheet.getImage(16, 12, self.width, self.height)
        images['Z'] = self.sheet.getImage(17, 12, self.width, self.height)

        images['0'] = self.sheet.getImage(18, 12, self.width, self.height)
        images['1'] = self.sheet.getImage(19, 12, self.width, self.height)
        images['2'] = self.sheet.getImage(20, 12, self.width, self.height)
        images['3'] = self.sheet.getImage(21, 12, self.width, self.height)
        images['4'] = self.sheet.getImage(16, 13, self.width, self.height)
        images['5'] = self.sheet.getImage(17, 13, self.width, self.height)
        images['6'] = self.sheet.getImage(18, 13, self.width, self.height)
        images['7'] = self.sheet.getImage(19, 13, self.width, self.height)
        images['8'] = self.sheet.getImage(20, 13, self.width, self.height)
        images['9'] = self.sheet.getImage(21, 13, self.width, self.height)
        images[' '] = None

        return images

    def convert(self, word):
        '''Convert a word to the corresponding images'''
        word = str(word)
        word = word.upper()
        textImages = []
        for i in range(len(word)):
            textImages.append(self.images[word[i]])
        return textImages
