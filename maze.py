import pygame
from constants import *
from vectors import Vector2D
from numpy import loadtxt

class Maze(object):
    def __init__(self, level, spritesheet):
        self.level = level
        self.spritesheet = spritesheet
        self.numMazes = len(MAZEDATA)
        self.skin = 16
        self.pieces = []
        self.extractMazeSprites()

    def extractMazeSprites(self):
        offset = self.level % self.numMazes
        print self.level, self.numMazes, offset
        for i in range(10):
            self.pieces.append(self.spritesheet.getImage(i, self.skin+offset, 16, 16))

    def fillMaze(self, background):
        level = self.level % self.numMazes
        self.grid = loadtxt(MAZEDATA[level]["file"], dtype=str)
        rows, cols = self.grid.shape
        for row in range(rows):
            for col in range(cols):
                x = col * 16
                y = row * 16
                for i in range(10):
                    for r in range(4):
                        if self.grid[row][col] == str(i)+str(r):
                            piece = self.rotate(self.pieces[i], r)
                            background.blit(piece, (x, y))


    def rotate(self, image, value):
        if value == 1:
            return pygame.transform.rotate(image, -90)
        elif value == 2:
            return pygame.transform.rotate(image, 180)
        elif value == 3:
            return pygame.transform.rotate(image, 90)
        else:
            return image
