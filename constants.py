from vectors import Vector2D

UP = Vector2D(0, -1)
DOWN = Vector2D(0, 1)
LEFT = Vector2D(-1, 0)
RIGHT = Vector2D(1, 0)
STOP = Vector2D()

WIDTH = 16
HEIGHT = 16
NROWS = 36
NCOLS = 28
SCREENSIZE = (NCOLS*WIDTH, NROWS*HEIGHT)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
MAROON = (255, 0, 100)
GREEN = (0, 255, 0)
LIGHTYELLOW = (250, 250, 100)
PINK = (255, 100, 150)
TEAL = (100, 255, 255)
ORANGE = (230, 190, 40)
TRANSPARENT = (255, 0, 255)

MAXSPEED = 100

MAZEDATA = {}
MAZEDATA[0] = {}
MAZEDATA[0]["file"] = "maze1.txt"
MAZEDATA[0]["portal"] = {(0, 17*HEIGHT):(27*WIDTH, 17*HEIGHT)}
MAZEDATA[0]["home"] = (15*WIDTH, 14*HEIGHT)
MAZEDATA[0]["start"] = {"pacman":(15*WIDTH, 26*HEIGHT), "ghost":(216, 272)}
MAZEDATA[0]["fruit"] = (18*WIDTH, 20*HEIGHT)
MAZEDATA[0]["restrictUp"] = {0:(12*WIDTH, 14*HEIGHT),
                             1:(15*WIDTH, 14*HEIGHT),
                             2:(12*WIDTH, 26*HEIGHT),
                             3:(15*WIDTH, 26*HEIGHT)}

MAZEDATA[1] = {}
MAZEDATA[1]["file"] = "maze2.txt"
MAZEDATA[1]["portal"] = {(0, 4*HEIGHT):(27*WIDTH, 4*HEIGHT),
                         (0, 26*HEIGHT):(27*WIDTH,26*HEIGHT)}
MAZEDATA[1]["home"] = ()
MAZEDATA[1]["start"] = {"pacman":(), "ghost":()}
MAZEDATA[1]["fruit"] = ()
MAZEDATA[1]["restrictUp"] = {}
        
