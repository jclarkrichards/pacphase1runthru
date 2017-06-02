import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *
from entities import MazeMouse
from animation import Animation, AnimationGroup

class Pacman(MazeMouse):
    def __init__(self, nodes, level, spritesheet):
        MazeMouse.__init__(self, nodes, level)
        self.name = "pacman"
        self.color = YELLOW
        self.setStartPosition()
        self.r = 4
        #self.image = pygame.image.load("Images/pacman.png").convert()
        #self.image.set_colorkey(TRANSPARENT)
        self.spritesheet = spritesheet
        #self.image = self.spritesheet.getImage(4, 0, 32, 32)
        self.pos = (self.position.x, self.position.y, 32, 32)
        self.previousDirection = self.direction

        self.animateName = "left"
        self.animate = AnimationGroup()
        self.defineAnimations()
        self.animate.setAnimation("left", 0)
        self.image = self.animate.getImage(0)
        self.alive = True
        self.deathSequenceFinished = False

    def update(self, dt):
        if self.alive:
            self.position += self.direction*self.speed*dt
            self.pos = (self.position.x, self.position.y, 32, 32)
            direction = self.getValidKey()

            if direction:
                self.moveByKey(direction)
            else:
                self.moveBySelf()

            self.checkDirectionChange()
        
            if self.direction != STOP:
                self.image = self.animate.ping(dt)
            else:
                self.image = self.animate.getImage(0)

        else:
            self.image = self.animate.onePass(dt)
            if self.animate.animation.finished:
                self.deathSequenceFinished = True
            
        
    def checkDirectionChange(self):
        if self.direction != self.previousDirection:
            self.previousDirection = self.direction
            if self.direction == LEFT:
                print "left"
                self.animateName = "left"
            elif self.direction == RIGHT:
                self.animateName = "right"
            elif self.direction == DOWN:
                self.animateName = "down"
            elif self.direction == UP:
                self.animateName = "up"
            self.animate.setAnimation(self.animateName, self.animate.animation.col)
            
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

    def defineAnimations(self):
        anim = Animation("left")
        anim.speed = 20
        anim.addFrame(self.spritesheet.getImage(4, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(0, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(0, 1, 32, 32))
        self.animate.add(anim)

        anim = Animation("right")
        anim.speed = 20
        anim.addFrame(self.spritesheet.getImage(4, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(1, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(1, 1, 32, 32))
        self.animate.add(anim)

        anim = Animation("down")
        anim.speed = 20
        anim.addFrame(self.spritesheet.getImage(4, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(2, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(2, 1, 32, 32))
        self.animate.add(anim)

        anim = Animation("up")
        anim.speed = 20
        anim.addFrame(self.spritesheet.getImage(4, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(3, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(3, 1, 32, 32))
        self.animate.add(anim)

        anim = Animation("death")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(0, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(1, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(2, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(3, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(4, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(5, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(6, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(7, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(8, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(9, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(10, 7, 32, 32))
        self.animate.add(anim)
        

