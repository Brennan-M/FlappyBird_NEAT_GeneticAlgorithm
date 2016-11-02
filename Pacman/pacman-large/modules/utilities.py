import pygame, sys, os, random
from modules.settings import *


def CheckInputs(player, thisGame, thisLevel): 
    
    if thisGame.mode == 1:
        if pygame.key.get_pressed()[ pygame.K_RIGHT ]:
            if not (player.velX == player.speed and player.velY == 0) and not thisLevel.CheckIfHitWall((player.x + player.speed, player.y), (player.nearestRow, player.nearestCol)): 
                player.velX = player.speed
                player.velY = 0
                
        elif pygame.key.get_pressed()[ pygame.K_LEFT ]:
            if not (player.velX == -player.speed and player.velY == 0) and not thisLevel.CheckIfHitWall((player.x - player.speed, player.y), (player.nearestRow, player.nearestCol)): 
                player.velX = -player.speed
                player.velY = 0
            
        elif pygame.key.get_pressed()[ pygame.K_DOWN ]:
            if not (player.velX == 0 and player.velY == player.speed) and not thisLevel.CheckIfHitWall((player.x, player.y + player.speed), (player.nearestRow, player.nearestCol)): 
                player.velX = 0
                player.velY = player.speed
            
        elif pygame.key.get_pressed()[ pygame.K_UP ]:
            if not (player.velX == 0 and player.velY == -player.speed) and not thisLevel.CheckIfHitWall((player.x, player.y - player.speed), (player.nearestRow, player.nearestCol)):
                player.velX = 0
                player.velY = -player.speed
            
    elif thisGame.mode == 3:
        if pygame.key.get_pressed()[ pygame.K_RETURN ]:
            thisGame.StartNewGame()
            


    




def CheckIfCloseButton(events):
    for event in events: 
        if event.type == QUIT: 
            sys.exit(0)
