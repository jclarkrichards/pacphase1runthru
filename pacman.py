import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *
from entities import MazeMouse

class Pacman(MazeMouse):
    def __init__(self, nodes, level, spritesheet):
        MazeMouse.__init__(self, nodes, level)
        self.name = "pacman"
        self.color = YELLOW
        self.imageRow = 0
        self.imageCol = 0
        self.animateFrame = 0
        self.setStartPosition()
        self.r = 4
        #self.image = pygame.image.load("Images/pacman.png").convert()
        #self.image.set_colorkey(TRANSPARENT)
        self.spritesheet = spritesheet
        self.image = self.spritesheet.getImage(4, 0, 32, 32)
        self.pos = (self.position.x, self.position.y, 32, 32)
        self.previousDirection = self.direction
        
    def update(self, dt):
        self.position += self.direction*self.speed*dt
        self.pos = (self.position.x, self.position.y, 32, 32)
        direction = self.getValidKey()
        if direction:
            self.moveByKey(direction)
        else:
            self.moveBySelf()

        self.checkDirectionChange()
        if self.direction != STOP:
            row, col = self.animate()
            self.animateFrame += 1
            if self.animateFrame > 5:
                self.animateFrame = 0
            self.setImage(row, col)
        else:
            self.setImage(0, 4)
        #print str(row)+", " + str(col)

    def animate(self):
        row = self.imageRow
        col = self.imageCol
        rowSequence = [0, 0, 1, 0, 1, 0]
        colSequence = [4] + [self.imageCol] * 5
        
        return rowSequence[self.animateFrame], colSequence[self.animateFrame]

    def checkDirectionChange(self):
        if self.direction != self.previousDirection:
            self.previousDirection = self.direction

            if self.direction == LEFT:
                self.imageCol = 0
            elif self.direction == RIGHT:
                self.imageCol = 1
            elif self.direction == DOWN:
                self.imageCol = 2
            elif self.direction == UP:
                self.imageCol = 3

    def setImage(self, row, col):
        self.image = self.spritesheet.getImage(col, row, 32, 32)   
            
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
