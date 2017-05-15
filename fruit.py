import pygame
from entities import MazeMouse
from constants import *

class CollectedFruit(MazeMouse):
    def __init__(self, nodes, level, displayedLevel):
        MazeMouse.__init__(self, nodes, level)
        self.name = "fruit"
        self.color = (0, 200, 0)
        self.chooser(displayedLevel)
        self.setStartPosition()
        self.value = 100

    def setStartPosition(self):
        pos = MAZEDATA[self.level]["fruit"]
        self.node = self.nodes.getNode(*pos, nodeList=self.nodes.nodeList)
        self.target = self.node.neighbors[LEFT]
        self.setPosition()
        halfway = (self.node.position.x - self.target.position.x) / 2
        self.position.x -= halfway

    def chooser(self, level):
        level %= 5
        if level == 0:
            self.name = "cherry"
            self.color = RED
            self.value = 100
            
        elif level == 1:
            self.name = "banana"
            self.color = YELLOW
            self.value = 200
            
        elif level == 2:
            self.name = "apple"
            self.color = MAROON
            self.value = 500
            
        elif level == 3:
            self.name = "watermelon"
            self.color = GREEN
            self.value = 1000
            
        elif level == 4:
            self.name = "lemon"
            self.color = LIGHTYELLOW
            self.value = 1500

class DisplayedFruit(object):
    def __init__(self, fruit):
        self.name = fruit.name
        self.color = fruit.color
        self.radius = fruit.radius

    def setPosition(self, index):
        x = WIDTH*NCOLS - (5 + self.radius + (2*self.radius + 5) * index)
        y = HEIGHT*(NROWS - 1)
        self.position = Vector2D(x, y)

    def render(self, screen):
        x, y = self.position.toTuple()
        pygame.draw.circle(screen, self.color, (x, y), self.radius)