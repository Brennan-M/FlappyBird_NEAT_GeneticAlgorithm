import pygame, sys, os, random
from modules.settings import *
from modules.utilities import *


class ANN_feed:

    def __init__(self):
        self.player = None
        self.ghosts = None
        self.fruit = None
        self.map = None


    def update(self, player, ghosts, fruit, map):
        self.player = player
        self.ghosts = ghosts
        self.fruit = fruit
        self.map = map

