import pygame
from entities import MazeMouse
from constants import *
from vectors import Vector2D
from random import randint
from stacks import Stack

class Mode(object):
    def __init__(self, name="", time=None, speedMult=1):
        self.name = name
        self.time = time
        self.speedMult = speedMult

        
class Ghost(MazeMouse):
    def __init__(self, nodes, level):
        MazeMouse.__init__(self, nodes, level)
        self.name = "ghost"
        self.goal = Vector2D()
        self.modeStack = self.setupModeStack()
        self.mode = self.modeStack.pop()
        self.modeTimer = 0
        #self.setStartPosition()
        self.homeNode = None
        self.startDirection = UP
        self.exitHome = True
        self.guideDog = False
        self.leftHome = True
        
    def getStartNode(self):
        node = MAZEDATA[self.level]["start"]["ghost"]
        return self.nodes.getNode(*node, nodeList=self.nodes.homeList)
    
    def update(self, dt, pacman, blinky):
        speedMod = self.modifySpeed()
        self.position += self.direction*speedMod*dt
        self.modeUpdate(dt)
        if self.mode.name == "CHASE":
            self.setChaseGoal(pacman, blinky)
        elif self.mode.name == "SCATTER":
            self.setScatterGoal()
        elif self.mode.name == "FREIGHT":
            self.setRandomGoal()
        elif self.mode.name == "SPAWN":
            self.setSpawnGoal()
        self.moveBySelf()

    def modifySpeed(self):
        if (self.node.portalNode is not None or
            self.target.portalNode is not None):
            return self.speed / 2.0
        return self.speed * self.mode.speedMult
    
    def setStartPosition(self):
        self.setHomeNode()
        #pos = MAZEDATA[self.level]["start"]["ghost"]
        #self.node = self.nodes.getNode(*pos, nodeList=self.nodes.homeList)
        self.direction = self.startDirection
        self.target = self.node.neighbors[self.direction]
        self.setPosition()
    
    def getValidDirections(self):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if not key == self.direction * -1:
                    validDirections.append(key)
        if len(validDirections) == 0:
            validDirections.append(self.forceBacktrack())

        if (self.node.home and DOWN in validDirections and
            self.mode.name != "SPAWN"):
            validDirections.remove(DOWN)
        if self.node.nowayUp and UP in validDirections:
            validDirections.remove(UP)

        if not self.leftHome:
            if self.exitHome:
                validDirections = self.guideOutOfHome(validDirections)
            else:
                validDirections = self.trapInHome(validDirections)
        return validDirections

    def trapInHome(self, validDirections):
        if LEFT in validDirections:
            validDirections.remove(LEFT)
        if RIGHT in validDirections:
            validDirections.remove(RIGHT)
        return validDirections

    def guideOutOfHome(self, validDirections):
        if not self.guideDog:
            if self.target == self.homeNode:
                self.guideDog = True
                validDirections = []
                validDirections.append(self.guideStack.pop())
        else:
            validDirections = []
            validDirections.append(self.guideStack.pop())
            if self.guideStack.isEmpty():
                self.guideDog = False
                self.leftHome = True
        return validDirections
                
    def getClosestDirection(self, validDirections):
        distances = []
        for direction in validDirections:
            diffVec = self.node.position + direction*WIDTH - self.goal
            distances.append(diffVec.magnitudeSquared())
        index = distances.index(min(distances))
        return validDirections[index]
        
    def randomDirection(self, validDirections):
        index = randint(0, len(validDirections) - 1)
        return validDirections[index]

    def moveBySelf(self):
        if self.overshotTarget():
            self.node = self.target
            self.portal()
            validDirections = self.getValidDirections()
            self.direction = self.getClosestDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()
            if self.mode.name == "SPAWN":
                if self.position == self.goal:
                    self.mode = self.modeStack.pop()

    def forceBacktrack(self):
        if self.direction * -1 == UP:
            return UP
        if self.direction * -1 == DOWN:
            return DOWN
        if self.direction * -1 == LEFT:
            return LEFT
        if self.direction * -1 == RIGHT:
            return RIGHT


    def setupModeStack(self):
        modes = Stack()
        modes.push(Mode(name="CHASE"))
        modes.push(Mode(name="SCATTER", time=5))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        return modes

    def setFreightMode(self):
        if self.mode.name != "FREIGHT" and self.mode.name != "SPAWN":
            if self.mode.time is not None:
                dt = self.mode.time - self.modeTimer
                self.modeStack.push(Mode(name=self.mode.name, time=dt))
            else:
                self.modeStack.push(Mode(name=self.mode.name))
            self.mode = Mode("FREIGHT", time=7, speedMult=0.5)
            self.modeTimer = 0
        elif self.mode.name == "FREIGHT":
            self.mode = Mode("FREIGHT", time=7, speedMult=0.5)
            self.modeTimer = 0
            
    def setScatterGoal(self):
        self.goal = Vector2D()

    def setChaseGoal(self, pacman, blinky=None):
        self.goal = pacman.position

    def setSpawnGoal(self):
        self.goal = self.homeNode.position
        
    def setRandomGoal(self):
        x = randint(0, NCOLS*WIDTH)
        y = randint(0, NROWS*HEIGHT)
        self.goal = Vector2D(x, y)
        
    def modeUpdate(self, dt):
        self.modeTimer += dt
        if self.mode.time is not None:
            if self.modeTimer >= self.mode.time:
                self.mode = self.modeStack.pop()
                self.modeTimer = 0

    def setRespawnMode(self):
        self.mode = Mode("SPAWN", speedMult=2)
        self.modeTimer = 0
        self.setGuideStack()
        self.leftHome = False
        
    def setGuideStack(self):
        self.guideStack = Stack()
        self.guideStack.push(LEFT)
        self.guideStack.push(UP)
        

class Blinky(Ghost):
    def __init__(self, nodes, level):
        Ghost.__init__(self, nodes, level)
        self.name = "blinky"
        self.color = RED
        self.startDirection = LEFT
        self.setStartPosition()
        
    def setScatterGoal(self):
        self.goal = Vector2D(WIDTH*NCOLS, 0)

    def setHomeNode(self):
        node = self.getStartNode()
        self.homeNode = node
        self.node = self.homeNode.neighbors[UP]

class Pinky(Ghost):
    def __init__(self, nodes, level):
        Ghost.__init__(self, nodes, level)
        self.name = "pinky"
        self.color = PINK
        self.setStartPosition()
        
    def setChaseGoal(self, pacman, blinky=None):
        self.goal = pacman.position + pacman.direction * WIDTH * 4
        
    def setScatterGoal(self):
        self.goal = Vector2D()

    def setHomeNode(self):
        node = self.getStartNode()
        self.homeNode = node
        self.node = node

class Inky(Ghost):
    def __init__(self, nodes, level):
        Ghost.__init__(self, nodes, level)
        self.name = "inky"
        self.color = TEAL
        self.startDirection = DOWN
        self.setStartPosition()
        self.exitHome = False
        self.setGuideStack()
        self.leftHome = False
        
    def setChaseGoal(self, pacman, blinky=None):
        vec1 = pacman.position + pacman.direction * WIDTH * 2
        vec2 = (vec1 - blinky.position) * 2
        self.goal = blinky.position + vec2
        
    def setScatterGoal(self):
        self.goal = Vector2D(0, HEIGHT*NROWS)

    def setHomeNode(self):
        node = self.getStartNode()
        self.homeNode = node.neighbors[LEFT]
        self.node = node.neighbors[LEFT]
        
    def setGuideStack(self):
        self.guideStack = Stack()
        self.guideStack.push(LEFT)
        self.guideStack.push(UP)
        self.guideStack.push(RIGHT)

        
class Clyde(Ghost):
    def __init__(self, nodes, level):
        Ghost.__init__(self, nodes, level)
        self.name = "clyde"
        self.color = ORANGE
        self.startDirection = DOWN
        self.setStartPosition()
        self.exitHome = False
        self.setGuideStack()
        self.leftHome = False
        
    def setChaseGoal(self, pacman, blinky=None):
        d = pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (WIDTH * 8)**2:
            self.setScatterGoal()
        else:
            self.goal = pacman.position
            
    def setScatterGoal(self):
        self.goal = Vector2D(WIDTH*NCOLS, HEIGHT*NROWS)

    def setHomeNode(self):
        node = self.getStartNode()
        self.homeNode = node.neighbors[RIGHT]
        self.node = node.neighbors[RIGHT]

    def setGuideStack(self):
        self.guideStack = Stack()
        self.guideStack.push(LEFT)
        self.guideStack.push(UP)
        self.guideStack.push(LEFT)
        
        
class GhostGroup(object):
    def __init__(self, nodes, level):
        self.nodes = nodes
        self.level = level
        self.ghosts = []
        self.ghosts = []
        self.ghosts.append(Blinky(nodes, level))
        self.ghosts.append(Pinky(nodes, level))
        self.ghosts.append(Inky(nodes, level))
        self.ghosts.append(Clyde(nodes, level))

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt, pacman):
        blinky = self.getGhost("blinky")
        for ghost in self:
            ghost.update(dt, pacman, blinky)

    def setFreightMode(self):
        for ghost in self:
            ghost.setFreightMode()

    def anyInFreight(self):
        for ghost in self:
            if ghost.mode.name == "FREIGHT":
                return True
        return False

    def anyInSpawn(self):
        for ghost in self:
            if ghost.mode.name == "SPAWN":
                return True
        return False

    def anyInFreightOrSpawn(self):
        for ghost in self:
            if (ghost.mode.name == "FREIGHT" or
                ghost.mode.name == "SPAWN"):
                return True
        return False

    def getGhost(self, name):
        for ghost in self:
            if ghost.name == name:
                return ghost
        return None

    def release(self, name):
        ghost = self.getGhost(name)
        if ghost is not None:
            ghost.exitHome = True
            
    def render(self,screen):
        for ghost in self:
            ghost.render(screen)