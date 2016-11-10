import pygame, sys, os, random
from modules.settings import *
from modules.utilities import *


class pacman ():
    
    def __init__ (self, path):
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = 3

        self.path = path
        
        self.nearestRow = 0
        self.nearestCol = 0
        
        self.homeX = 0
        self.homeY = 0
        
        self.anim_pacmanL = {}
        self.anim_pacmanR = {}
        self.anim_pacmanU = {}
        self.anim_pacmanD = {}
        self.anim_pacmanS = {}
        self.anim_pacmanCurrent = {}
        
        for i in range(1, 9, 1):
            self.anim_pacmanL[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-l " + str(i) + ".gif")).convert()
            self.anim_pacmanR[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-r " + str(i) + ".gif")).convert()
            self.anim_pacmanU[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-u " + str(i) + ".gif")).convert()
            self.anim_pacmanD[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-d " + str(i) + ".gif")).convert()
            self.anim_pacmanS[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman.gif")).convert()

        self.pelletSndNum = 0
        
    def Move (self, thisLevel, ghosts, thisFruit, thisGame):
        
        self.nearestRow = int(((self.y + (TILE_WIDTH/2)) / TILE_WIDTH))
        self.nearestCol = int(((self.x + (TILE_HEIGHT/2)) / TILE_HEIGHT))

        # make sure the current velocity will not cause a collision before moving
        if not thisLevel.CheckIfHitWall((self.x + self.velX, self.y + self.velY), (self.nearestRow, self.nearestCol)):
            # it's ok to Move
            self.x += self.velX
            self.y += self.velY
            
            # check for collisions with other tiles (pellets, etc)
            thisLevel.CheckIfHitSomething((self.x, self.y), (self.nearestRow, self.nearestCol), thisGame)
            
            # check for collisions with the ghosts
            for i in range(0, 4, 1):
                if thisLevel.CheckIfHit( (self.x, self.y), (ghosts[i].x, ghosts[i].y), TILE_WIDTH/2):
                    # hit a ghost
                    
                    if ghosts[i].state == 1:
                        # ghost is normal
                        thisGame.SetMode( 2 )
                        
                    elif ghosts[i].state == 2:
                        # ghost is vulnerable
                        # give them glasses
                        # make them run
                        thisGame.AddToScore(thisGame.ghostValue)
                        thisGame.ghostValue = thisGame.ghostValue * 2
                        #snd_eatgh.play()
                        
                        ghosts[i].state = 3
                        ghosts[i].speed = ghosts[i].speed * 4
                        # and send them to the ghost box
                        ghosts[i].x = ghosts[i].nearestCol * TILE_WIDTH
                        ghosts[i].y = ghosts[i].nearestRow * TILE_HEIGHT
                        ghosts[i].currentPath = self.path.FindPath( (ghosts[i].nearestRow, ghosts[i].nearestCol), (thisLevel.GetGhostBoxPos()[0]+1, thisLevel.GetGhostBoxPos()[1]) )
                        ghosts[i].FollowNextPathWay(self, thisLevel)
                        
                        # set game mode to brief pause after eating
                        thisGame.SetMode( 5 )
                        
            # check for collisions with the fruit
            if thisFruit.active == True:
                if thisLevel.CheckIfHit( (self.x, self.y), (thisFruit.x, thisFruit.y), TILE_WIDTH/2):
                    thisGame.AddToScore(2500)
                    thisFruit.active = False
                    thisGame.fruitTimer = 0
                    thisGame.fruitScoreTimer = 120
                    #snd_eatfruit.play()
        
        else:
            # we're going to hit a wall -- stop moving
            self.velX = 0
            self.velY = 0
            
        # deal with power-pellet ghost timer
        if thisGame.ghostTimer > 0:
            thisGame.ghostTimer -= 1
            
            if thisGame.ghostTimer == 0:
                for i in range(0, 4, 1):
                    if ghosts[i].state == 2:
                        ghosts[i].state = 1
                self.ghostValue = 0
                
        # deal with fruit timer
        thisGame.fruitTimer += 1
        if thisGame.fruitTimer == 500:
            pathwayPair = thisLevel.GetPathwayPairPos()
            
            if not pathwayPair == False:
            
                pathwayEntrance = pathwayPair[0]
                pathwayExit = pathwayPair[1]
                
                thisFruit.active = True
                
                thisFruit.nearestRow = pathwayEntrance[0]
                thisFruit.nearestCol = pathwayEntrance[1]
                
                thisFruit.x = thisFruit.nearestCol * TILE_WIDTH
                thisFruit.y = thisFruit.nearestRow * TILE_HEIGHT
                
                thisFruit.currentPath = self.path.FindPath( (thisFruit.nearestRow, thisFruit.nearestCol), pathwayExit )
                thisFruit.FollowNextPathWay()
            
        if thisGame.fruitScoreTimer > 0:
            thisGame.fruitScoreTimer -= 1
            
        
    def Draw (self, thisGame):
        
        if thisGame.mode == 3:
            return False
        
        # set the current frame array to match the direction pacman is facing
        if self.velX > 0:
            self.anim_pacmanCurrent = self.anim_pacmanR
        elif self.velX < 0:
            self.anim_pacmanCurrent = self.anim_pacmanL
        elif self.velY > 0:
            self.anim_pacmanCurrent = self.anim_pacmanD
        elif self.velY < 0:
            self.anim_pacmanCurrent = self.anim_pacmanU
            
        screen.blit (self.anim_pacmanCurrent[ self.animFrame ], (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))
        
        if thisGame.mode == 1:
            if not self.velX == 0 or not self.velY == 0:
                # only Move mouth when pacman is moving
                self.animFrame += 1 
            
            if self.animFrame == 9:
                # wrap to beginning
                self.animFrame = 1
            