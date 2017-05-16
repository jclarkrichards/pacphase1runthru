import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from ghosts import GhostGroup
from pellets import PelletGroup
from fruit import CollectedFruit, DisplayedFruit
from lifeicons import Lives

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        #self.setBackGround()
        self.clock = pygame.time.Clock()
        self.level = 0
        self.score = 0
        self.ghostScore = 200
        self.lives = 5
        self.idleTimer = 0
        self.displayedFruits = []
        self.displayedLevel = 0
        self.maxLevels = 2
        self.startDelay= False
        self.restartDelay = False
        self.lifeIcons = Lives()
        #self.imLife = pygame.image.load("Images/pacman.png").convert()
        #self.imLife.set_colorkey(WHITE)
        #print self.imLife.get_rect()

    def setBackGround(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)
        self.nodes = NodeGroup(self.level)
        self.nodes.render(self.background)
        self.screen.blit(self.background, (0,0))
        #self.lifeIcons = Lives()
        #print "Background"
        #print self.background.get_size()
        #pygame.draw.circle(self.background, GREEN, (150, 432), 5)
        #pygame.draw.circle(self.background, GREEN, (180, 432), 5)
        #self.screen.blit(self.background, (0, 0))

    def startGame(self):
        self.setBackGround()
        #self.nodes = NodeGroup(self.level)
        self.pellets = PelletGroup(self.level)
        self.pacman = Pacman(self.nodes, self.level)
        self.ghosts = GhostGroup(self.nodes, self.level)
        self.fruit = None
        self.fruitTimer = 0
        self.paused = True
        self.pauseTimer = 0
        self.pauseTime = 0
        self.playerPaused = True
        self.startDelay = False
        #self.nodes.render(self.background)
        #self.screen.blit(self.background, (0, 0))

    def restartLevel(self):
        self.pacman = Pacman(self.nodes, self.level)
        self.ghosts = GhostGroup(self.nodes, self.level)
        self.paused = True
        self.fruit =None
        self.fruitTimer = 0
        self.pauseTimer = 0
        self.pauseTime = 0
        self.playerPaused = True
        self.restartDelay = False
        #self.nodes.render(self.background)
        #self.screen.blit(self.background, (0, 0))

    def update(self):
        dt = self.clock.tick(30)/1000.0
        if not self.paused:
            #print self.pacman.pos
            #self.screen.blit(self.background, self.pacman.pos, self.pacman.pos)
            
            self.pacman.update(dt)
            self.ghosts.update(dt, self.pacman)
            self.checkPelletEvents(dt)
            self.checkGhostEvents(dt)
            self.checkFruitEvents(dt)
        else:
            if not self.playerPaused:
                self.pauseTimer += dt
                if self.pauseTimer >= self.pauseTime:
                    self.paused = False
                    if self.startDelay == True:
                        self.startGame()
                    if self.restartDelay == True:
                        self.restartLevel()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.paused:
                        #self.paused = False
                        self.playerPaused = False
                    else:
                        #self.paused = True
                        self.playerPaused = True
                    self.paused = not self.paused
                    
    def checkPelletEvents(self, dt):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)        
        if pellet:
            #print self.pellets.numEaten
            self.pellets.numEaten += 1
            self.idleTimer = 0
            self.score += pellet.value
            self.pellets.pelletList.remove(pellet)
            if pellet.name == "powerpellet":
                self.ghostScore = 200
                self.ghosts.setFreightMode()
            if self.pellets.isEmpty():
                self.paused = True
                self.pauseTime = 3
                self.pauseTimer = 0
                self.startDelay = True
                self.increaseLevel()

            if self.ghosts.anyInFreightOrSpawn():
                self.pacman.boostSpeed()
            else:
                self.pacman.reduceSpeed()
            if (self.pellets.numEaten == 70 or
                self.pellets.numEaten == 140):
                self.fruit = CollectedFruit(self.nodes, self.level,
                                            self.displayedLevel)

        else:
            self.idleTimer += dt
            if self.ghosts.anyInFreightOrSpawn():
                self.pacman.boostSpeed()
            else:
                if self.idleTimer >= 0.5:
                    self.pacman.normalSpeed()
                
    def checkGhostEvents(self, dt):
        ghost = self.pacman.eatGhost(self.ghosts)
        if ghost is not None:
            if ghost.mode.name == "FREIGHT":
                self.score += self.ghostScore
                self.ghostScore *= 2
                ghost.setRespawnMode()
                self.paused = True
                self.pauseTime = 0.5
                self.pauseTimer = 0
            elif ghost.mode.name != "SPAWN":
                self.paused = True
                self.pauseTime = 1
                self.pauseTimer = 0
                self.restartDelay = True
                self.lives -= 1
                if self.lives == 0:
                    self.level = 0
                    self.lives = 5
                    self.startGame()


        if self.pellets.numEaten >= 30 or self.idleTimer >= 10:
            self.ghosts.release("inky")
        if self.pellets.numEaten >= 60 or self.idleTimer >= 10:
            self.ghosts.release("clyde")

    def checkFruitEvents(self, dt):
        if self.fruit is not None:
            if self.pacman.eatFruit(self.fruit):
                self.score += self.fruit.value
                self.addDisplayedFruit()
                self.fruitTimer = 0
                self.fruit = None
            else:
                self.fruitTimer += dt
                if self.fruitTimer >= 10:
                    self.fruitTimer = 0
                    self.fruit = None

    def addDisplayedFruit(self):
        fruitNames = [n.name for n in self.displayedFruits]
        if self.fruit.name not in fruitNames:
            fruit = DisplayedFruit(self.fruit)
            fruit.setPosition(len(self.displayedFruits))
            self.displayedFruits.append(fruit)
            
    def increaseLevel(self):
        self.level += 1
        self.displayedLevel += 1
        self.level %= self.maxLevels
        
    def render(self):
        self.screen.blit(self.background, (0, 0))
        #self.nodes.render(self.screen)
        #p = (self.pacman.position.x, self.pacman.position.y, 32, 32)
        #print p

        #self.screen.blit(self.pacman.image, self.pacman.pos)
        
        #self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        for fruit in self.displayedFruits:
            fruit.render(self.screen)
            
        #p = self.pacman.image.get_rect()
        #self.screen.blit(self.background, p, p)
        #self.screen.blit(self.pacman.image, p)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.lifeIcons.render(self.screen, self.lives-1)
        
        #for i in range(self.lives - 1):
        #    width = self.imLife.get_rect()[2]
            #y = HEIGHT * (NROWS - 1)
        #    y = HEIGHT * (NROWS - 2)
        #    x = 5 + (width + 5)*i
            #x = 5 + self.pacman.radius + (2*self.pacman.radius + 5)*i
        #    self.screen.blit(self.imLife, (x, y))
            #pygame.draw.circle(self.screen, self.pacman.color, (x, y),
            #                   self.pacman.radius)
        pygame.display.update()
        #pygame.display.update(pacrect)
        
        #pygame.display.flip()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
