#! /usr/bin/python

# pacman.pyw
# By David Reilly
# Modified Version by Andy Sommerville (Oct. 8th, 2007)

# Modified by Michael Iuzzolino, 1 November 2016:
# - Cleaned code and broke apart into modules
# - Removed joystick support
# - Revamping game towards interface with neural networks

import pygame, sys, os, random
from pygame.locals import *
from modules.settings import *
from modules.game import *
from modules.level import *
from modules.ghost import *
from modules.fruit import *
from modules.pacman import *
from modules.pathfinder import *
from modules.ANN_feed import *


def main():
    # create a path_finder object
    path = path_finder()

    # create feed to ANN
    ann_feed = ANN_feed()

    # create the pacman
    player = pacman(path)

    # create ghost objects
    ghosts = {}
    for i in range(0, 6, 1):
        # remember, ghost[4] is the blue, vulnerable ghost
        ghosts[i] = ghost(i, path)
        
    # create piece of fruit
    thisFruit = fruit()

    # create game and level objects and load first level
    thisLevel = level(path, player, thisFruit, ghosts)
    thisGame = game(path, player, ghosts, thisFruit, thisLevel, ann_feed)
    thisGame.LoadLevel()

    window = pygame.display.set_mode( thisGame.screenSize, pygame.HWSURFACE | pygame.DOUBLEBUF )

    while True: 

        CheckIfCloseButton( pygame.event.get() )
        thisGame.Play()


if __name__ == "__main__":
    main()
    
