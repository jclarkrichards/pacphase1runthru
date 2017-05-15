import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *
from entities import MazeMouse

class Pacman(MazeMouse):
    def __init__(self, nodes, level):
        MazeMouse.__init__(self, nodes, level)
        self.name = "pacman"
        self.color = YELLOW
        self.setStartPosition()
        self.r = 4

    def update(self, dt):
        self.position += self.direction*self.speed*dt
        direction = self.getValidKey()
        if direction:
            self.moveByKey(direction)
        else:
            self.moveBySelf()


    def setStartPosition(self):
        self.direction = LEFT
        pos = MAZEDATA[self.level]["start"]["pacman"]
        self.node = self.nodes.getNode(*pos, nodeList=self.nodes.nodeList)
        self.target = self.node.neighbors[self.direction]
        self.setPosition()
        halfway = (self.node.position.x - self.target.position.x) / 2
        self.position.x -= halfway
        
    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        else:
            return None

    def moveByKey(self, direction):
        if self.direction is STOP:
            if self.node.neighbors[direction] is not None:
                self.target = self.node.neighbors[direction]
                self.direction = direction
        else:
            if direction == self.direction * -1:
                self.reverseDirection()
            if self.overshotTarget():
                self.node = self.target
                self.portal()
                if (self.node.neighbors[direction] is not None and
                    not self.node.home):
                    self.target = self.node.neighbors[direction]
                    if self.direction != direction:
                        self.setPosition()
                        self.direction = direction
                else:
                    if self.node.neighbors[self.direction] is not None:
                        self.target = self.node.neighbors[self.direction]
                    else:
                        self.setPosition()
                        self.direction = STOP

    def eatObject(self, obj):
        d = self.position - obj.position
        dSquared = d.magnitudeSquared()
        rSquared = 4 * self.r**2
        if dSquared <= rSquared:
            return True
        return False

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.eatObject(pellet):
                return pellet
        return None

    def eatGhost(self, ghosts):
        for ghost in ghosts:
            if self.eatObject(ghost):
                return ghost
        return None

    def eatFruit(self, fruit):
        return self.eatObject(fruit)
        
    def boostSpeed(self):
        self.speed = MAXSPEED * 1.5

    def normalSpeed(self):
        self.speed = MAXSPEED

    def reduceSpeed(self):
        self.speed = MAXSPEED * 0.8
