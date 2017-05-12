import pygame
from pygame.locals import *
from constants import *

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = None
        self.background = None
        self.setBackGround()

    def setBackGround(self):
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        pass

    def update(self):
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
