import pygame
from vectors import Vector2D
from constants import *

class MazeMouse(object):
    def __init__(self, nodes, level):
        self.name = ""
        self.nodes = nodes
        self.node = nodes.nodeList[0]
        self.target = self.node
        self.setPosition()
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.color = WHITE
        self.level = level
        self.image = None

    def setPosition(self):
        self.position = self.node.position.copy()

    def update(self, dt):
        self.position += self.direction*self.speed*dt
        self.moveBySelf()

    def moveBySelf(self):
        if self.direction is not STOP:
            if self.overshotTarget():
                self.node = self.target
                self.portal()
                if self.node.neighbors[self.direction] is not None:
                    self.target = self.node.neighbors[self.direction]
                else:
                    self.setPosition()
                    self.direction = STOP

    def overshotTarget(self):
        vec1 = self.target.position - self.node.position
        vec2 = self.position - self.node.position
        node2Target = vec1.magnitudeSquared()
        node2Self = vec2.magnitudeSquared()
        return node2Self >= node2Target

    def reverseDirection(self):
        if self.direction is UP: self.direction = DOWN
        elif self.direction is DOWN: self.direction = UP
        elif self.direction is LEFT: self.direction = RIGHT
        elif self.direction is RIGHT: self.direction = LEFT
        temp = self.node
        self.node = self.target
        self.target = temp

    def setNextTarget(self, direction):
        self.target = self.node.neighbors[direction]
        self.direction = direction
        
    def portal(self):
        if self.node.portalNode:
            self.node = self.node.portalNode
            self.setPosition()

    def render(self, screen):
        px = int(self.position.x)
        py = int(self.position.y)
        if self.image is not None:
            screen.blit(self.image, (px, py))
        else:
            pygame.draw.circle(screen, self.color, (px, py), self.radius)
