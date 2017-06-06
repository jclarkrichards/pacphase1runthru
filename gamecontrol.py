import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from ghosts import GhostGroup
from pellets import PelletGroup
from fruit import CollectedFruit, DisplayedFruit
from lifeicons import Lives
from spritesheet import SpriteSheet
from maze import Maze
from text2 import TextGroup

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.level = 0
        self.score = 0
        self.scoreAccumulator = 0
        self.maxLives = 5
        self.newLifePoints = 10000
        self.ghostScore = 200
        self.lives = 5
        self.idleTimer = 0
        self.displayedFruits = []
        self.displayedLevel = 0
        self.maxLevels = 2
        self.startDelay= False
        self.restartDelay = False
        self.sheet = SpriteSheet()
        self.lifeIcons = Lives(self.sheet)

        self.allText = TextGroup()
        self.allText.add("hi_score_label", "HI SCORE", align="left")
        self.allText.add("score_label", "SCORE", align="center")
        self.allText.add("level_label", "LEVEL", align="right")
        self.allText.add("start_label", "START", y=20*HEIGHT, align="center", color=RED)
        self.allText.add("score", self.score, y=HEIGHT, align = "center")
        self.allText.add("level", self.displayedLevel, y=HEIGHT, align = "right")

    def setBackGround(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackGround()
        self.maze = Maze(self.level, self.sheet)
        self.maze.fillMaze(self.background)
        self.nodes = NodeGroup(self.level)
        self.pellets = PelletGroup(self.level)
        self.pacman = Pacman(self.nodes, self.level, self.sheet)
        self.ghosts = GhostGroup(self.nodes, self.level, self.sheet)
        self.fruit = None
        self.fruitTimer = 0
        self.paused = True
        self.pauseTimer = 0
        self.pauseTime = 0
        self.playerPaused = True
        self.startDelay = False
        self.scoreAccumulator = 0
        
    def restartLevel(self):
        self.pacman = Pacman(self.nodes, self.level, self.sheet)
        self.ghosts = GhostGroup(self.nodes, self.level, self.sheet)
        self.paused = True
        self.fruit =None
        self.fruitTimer = 0
        self.pauseTimer = 0
        self.pauseTime = 0
        self.playerPaused = True
        self.restartDelay = False
        self.scoreAccumulator = 0
        
    def update(self):
        dt = self.clock.tick(30)/1000.0
        #self.screen.blit(self.background, self.pacman.pos, self.pacman.pos)        
        if not self.paused:
            self.allText.remove("ghost_score")
            self.pacman.update(dt)
            self.ghosts.update(dt, self.pacman)
            self.checkPelletEvents(dt)
            self.checkGhostEvents(dt)
            self.checkFruitEvents(dt)
            self.applyScore()
        else:
            if not self.playerPaused:
                if not self.pacman.alive:
                    #self.pacman.alive = False
                    self.pacman.update(dt)
                    if self.pacman.deathSequenceFinished:
                        if self.lives > 0:
                            self.restartLevel()
                        else:
                            self.allText.add("game_over_label", "GAME OVER", 
                                             y=20*HEIGHT, align="center", color=RED)
                else:
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
                    self.allText.remove("start_label")
                    if self.paused:
                        self.playerPaused = False
                        self.allText.remove("paused_label")
                    else:
                        self.playerPaused = True
                        self.allText.add("paused_label", "PAUSED", y=20*HEIGHT, align="center", color=GREEN)
                    self.paused = not self.paused
                    
    def checkPelletEvents(self, dt):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)        
        if pellet:
            #print self.pellets.numEaten
            self.pellets.numEaten += 1
            self.idleTimer = 0
            self.scoreAccumulator += pellet.value
            #self.score += pellet.value
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
                                            self.displayedLevel, self.sheet)

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
                #self.score += self.ghostScore
                self.allText.add("ghost_score", self.ghostScore, x=self.pacman.position.x, y=self.pacman.position.y, size=0.5)
                self.scoreAccumulator += self.ghostScore
                self.ghostScore *= 2
                ghost.setRespawnMode()
                self.paused = True
                self.pauseTime = 0.5
                self.pauseTimer = 0
            elif ghost.mode.name != "SPAWN":
                self.paused = True
                #self.lostLife = True
                #self.pauseTime = 1
                #self.pauseTimer = 0
                self.restartDelay = True
                self.lives -= 1
                self.pacman.alive = False
                self.pacman.animate.setAnimation("death", 0)
                #if self.lives == 0:
                #    self.level = 0
                #    self.lives = 5
                #    self.startGame()


        if self.pellets.numEaten >= 30 or self.idleTimer >= 10:
            self.ghosts.release("inky")
        if self.pellets.numEaten >= 60 or self.idleTimer >= 10:
            self.ghosts.release("clyde")

    def checkFruitEvents(self, dt):
        if self.fruit is not None:
            if self.pacman.eatFruit(self.fruit):
                #self.score += self.fruit.value
                self.scoreAccumulator += self.fruit.value
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
        self.allText.remove("level")
        self.displayedLevel += 1
        self.allText.add("level", self.displayedLevel, y=HEIGHT, align="right")
        self.level %= self.maxLevels

    def applyScore(self):
        if self.scoreAccumulator > 0:
            newScore = self.score + self.scoreAccumulator
        
            if ((newScore % 10000 - self.score % 10000) < 0 or
                newScore - self.score >= 10000):
                if self.lives < self.maxLives:
                    self.lives += 1

            #print "Old score = " + str(self.score)
            self.allText.remove("score")
            self.score = newScore #+= self.scoreAccumulator
            #print "New Score = " + str(self.score)
            #print ""
            self.allText.add("score", self.score, y=HEIGHT, align="center")
            #self.allText.update(self.score, self.score, align="center")
            self.scoreAccumulator = 0
        
    
    def render(self):
        self.screen.blit(self.background, (0, 0))
        #p = (self.pacman.position.x, self.pacman.position.y, 32, 32)
        #print p

        #self.screen.blit(self.pacman.image, self.pacman.pos)
        
        #self.nodes.render(self.screen)
        for fruit in self.displayedFruits:
            fruit.render(self.screen)
        self.pellets.render(self.screen)
            
        if not self.paused:
            if self.fruit is not None:
                self.fruit.render(self.screen)
            self.pacman.render(self.screen)
            if self.pacman.alive:
                self.ghosts.render(self.screen)
        else:
            if not self.pacman.alive:
                self.pacman.render(self.screen)

        self.lifeIcons.render(self.screen, self.lives-1)

        self.allText.render(self.screen)

        #label = self.font.render(str(self.score), 1, (255, 0, 0))
        #self.screen.blit(label, (0,0))
        pygame.display.update()
        #pygame.display.update(pacrect)
        
        #pygame.display.flip()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
