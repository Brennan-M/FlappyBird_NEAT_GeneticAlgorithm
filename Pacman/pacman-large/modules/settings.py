import pygame, sys, os, random
from pygame.locals import *


tileIDName = {} # gives tile name (when the ID# is known)
tileID = {} # gives tile ID (when the name is known)
tileIDImage = {} # gives tile image (when the ID# is known)

# WIN???
SCRIPT_PATH=sys.path[0]

TILE_WIDTH=TILE_HEIGHT=24

# NO_GIF_TILES -- tile numbers which do not correspond to a GIF file
# currently only "23" for the high-score list
NO_GIF_TILES=[23]

NO_WX=0 # if set, the high-score code will not attempt to ask the user his name
USER_NAME="User" # USER_NAME=os.getlogin() # the default user name if wx fails to load or NO_WX
                 # Oops! os.getlogin() only works if you launch from a terminal
# constants for the high-score display
HS_FONT_SIZE=14
HS_LINE_HEIGHT=16
HS_WIDTH=408
HS_HEIGHT=120
HS_XOFFSET=48
HS_YOFFSET=384
HS_ALPHA=200

# new constants for the score's position
SCORE_XOFFSET=50 # pixels from left edge
SCORE_YOFFSET=34 # pixels from bottom edge (to top of score)
SCORE_COLWIDTH=13 # width of each character


# See GetCrossRef() -- where these colors occur in a GIF, they are replaced according to the level file
IMG_EDGE_LIGHT_COLOR = (0xff,0xce,0xff,0xff)
IMG_FILL_COLOR = (0x84,0x00,0x84,0xff)
IMG_EDGE_SHADOW_COLOR = (0xff,0x00,0xff,0xff)
IMG_PELLET_COLOR = (0x80,0x00,0x80,0xff)




clock = pygame.time.Clock()
pygame.init()

window = pygame.display.set_mode((1, 1))
pygame.display.set_caption("Pacman")

screen = pygame.display.get_surface()

img_Background = pygame.image.load(os.path.join(SCRIPT_PATH,"res","backgrounds","1.gif")).convert()

# Initial joystick
js = None

ghostcolor = {}
ghostcolor[0] = (255, 0, 0, 255)
ghostcolor[1] = (255, 128, 255, 255)
ghostcolor[2] = (128, 255, 255, 255)
ghostcolor[3] = (255, 128, 0, 255)
ghostcolor[4] = (50, 50, 255, 255) # blue, vulnerable ghost
ghostcolor[5] = (255, 255, 255, 255) # white, flashing ghost