import pygame, sys, os, random
from modules.settings import *
from modules.utilities import *
class level ():
    
    def __init__ (self, path, player, thisFruit, ghosts):
        self.lvlWidth = 0
        self.lvlHeight = 0
        self.edgeLightColor = (255, 255, 0, 255)
        self.edgeShadowColor = (255, 150, 0, 255)
        self.fillColor = (0, 255, 255, 255)
        self.pelletColor = (255, 255, 255, 255)

        self.path = path
        self.player = player
        self.thisFruit = thisFruit
        self.ghosts = ghosts


        self.map = {}
        
        self.pellets = 0
        self.powerPelletBlinkTimer = 0
        
    def SetMapTile (self, (row, col), newValue):
        self.map[ (row * self.lvlWidth) + col ] = newValue
        
    def GetMapTile (self, (row, col)):
        if row >= 0 and row < self.lvlHeight and col >= 0 and col < self.lvlWidth:
            return self.map[ (row * self.lvlWidth) + col ]
        else:
            return 0
    
    def IsWall (self, (row, col)):
    
        if row > self.lvlHeight - 1 or row < 0:
            return True
        
        if col > self.lvlWidth - 1 or col < 0:
            return True
    
        # check the offending tile ID
        result = self.GetMapTile((row, col))

        # if the tile was a wall
        if result >= 100 and result <= 199:
            return True
        else:
            return False
    
                    
    def CheckIfHitWall (self, (possiblePlayerX, possiblePlayerY), (row, col)):
    
        numCollisions = 0
        
        # check each of the 9 surrounding tiles for a collision
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):
            
                if  (possiblePlayerX - (iCol * TILE_WIDTH) < TILE_WIDTH) and (possiblePlayerX - (iCol * TILE_WIDTH) > -TILE_WIDTH) and (possiblePlayerY - (iRow * TILE_HEIGHT) < TILE_HEIGHT) and (possiblePlayerY - (iRow * TILE_HEIGHT) > -TILE_HEIGHT):
                    
                    if self.IsWall((iRow, iCol)):
                        numCollisions += 1
                        
        if numCollisions > 0:
            return True
        else:
            return False
        
        
    def CheckIfHit (self, (playerX, playerY), (x, y), cushion):
    
        if (playerX - x < cushion) and (playerX - x > -cushion) and (playerY - y < cushion) and (playerY - y > -cushion):
            return True
        else:
            return False


    def CheckIfHitSomething (self, (playerX, playerY), (row, col), thisGame):
    
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):
            
                if  (playerX - (iCol * TILE_WIDTH) < TILE_WIDTH) and (playerX - (iCol * TILE_WIDTH) > -TILE_WIDTH) and (playerY - (iRow * TILE_HEIGHT) < TILE_HEIGHT) and (playerY - (iRow * TILE_HEIGHT) > -TILE_HEIGHT):
                    # check the offending tile ID
                    result = self.GetMapTile((iRow, iCol))
        
                    if result == tileID[ 'pellet' ]:
                        # got a pellet
                        self.SetMapTile((iRow, iCol), 0)
                        #snd_pellet[player.pelletSndNum].play()
                        self.player.pelletSndNum = 1 - self.player.pelletSndNum
                        
                        self.pellets -= 1
                        
                        thisGame.AddToScore(10)
                        
                        if self.pellets == 0:
                            # no more pellets left!
                            # WON THE LEVEL
                            thisGame.SetMode( 6 )
                            
                        
                    elif result == tileID[ 'pellet-power' ]:
                        # got a power pellet
                        self.SetMapTile((iRow, iCol), 0)
                        pygame.mixer.stop()
                        #snd_powerpellet.play()
                        
                        thisGame.AddToScore(100)
                        thisGame.ghostValue = 200
                        
                        thisGame.ghostTimer = 360
                        for i in range(0, 4, 1):
                            if self.ghosts[i].state == 1:
                                self.ghosts[i].state = 2
                                
                                """
                                # Must line up with grid before invoking a new path (for now)
                                ghosts[i].x = ghosts[i].nearestCol * TILE_HEIGHT
                                ghosts[i].y = ghosts[i].nearestRow * TILE_WIDTH                             
                                
                                # give each ghost a path to a random spot (containing a pellet)
                                (randRow, randCol) = (0, 0)

                                while not self.GetMapTile((randRow, randCol)) == tileID[ 'pellet' ] or (randRow, randCol) == (0, 0):
                                    randRow = random.randint(1, self.lvlHeight - 2)
                                    randCol = random.randint(1, self.lvlWidth - 2)
                                ghosts[i].currentPath = path.FindPath( (ghosts[i].nearestRow, ghosts[i].nearestCol), (randRow, randCol) )
                                
                                ghosts[i].FollowNextPathWay()
                                """
                        
                    elif result == tileID[ 'door-h' ]:
                        # ran into a horizontal door
                        for i in range(0, self.lvlWidth, 1):
                            if not i == iCol:
                                if self.GetMapTile((iRow, i)) == tileID[ 'door-h' ]:
                                    self.player.x = i * TILE_WIDTH
                                    
                                    if self.player.velX > 0:
                                        self.player.x += TILE_WIDTH
                                    else:
                                        self.player.x -= TILE_WIDTH
                                        
                    elif result == tileID[ 'door-v' ]:
                        # ran into a vertical door
                        for i in range(0, self.lvlHeight, 1):
                            if not i == iRow:
                                if self.GetMapTile((i, iCol)) == tileID[ 'door-v' ]:
                                    self.player.y = i * TILE_HEIGHT
                                    
                                    if self.player.velY > 0:
                                        self.player.y += TILE_HEIGHT
                                    else:
                                        self.player.y -= TILE_HEIGHT
                                        
    def GetGhostBoxPos (self):
        
        for row in range(0, self.lvlHeight, 1):
            for col in range(0, self.lvlWidth, 1):
                if self.GetMapTile((row, col)) == tileID[ 'ghost-door' ]:
                    return (row, col)
                
        return False
    
    def GetPathwayPairPos (self):
        
        doorArray = []
        
        for row in range(0, self.lvlHeight, 1):
            for col in range(0, self.lvlWidth, 1):
                if self.GetMapTile((row, col)) == tileID[ 'door-h' ]:
                    # found a horizontal door
                    doorArray.append( (row, col) )
                elif self.GetMapTile((row, col)) == tileID[ 'door-v' ]:
                    # found a vertical door
                    doorArray.append( (row, col) )
        
        if len(doorArray) == 0:
            return False
        
        chosenDoor = random.randint(0, len(doorArray) - 1)
        
        if self.GetMapTile( doorArray[chosenDoor] ) == tileID[ 'door-h' ]:
            # horizontal door was chosen
            # look for the opposite one
            for i in range(0, self.lvlWidth, 1):
                if not i == doorArray[chosenDoor][1]:
                    if self.GetMapTile((doorArray[chosenDoor][0], i)) == tileID[ 'door-h' ]:
                        return doorArray[chosenDoor], (doorArray[chosenDoor][0], i)
        else:
            # vertical door was chosen
            # look for the opposite one
            for i in range(0, self.lvlHeight, 1):
                if not i == doorArray[chosenDoor][0]:
                    if self.GetMapTile((i, doorArray[chosenDoor][1])) == tileID[ 'door-v' ]:
                        return doorArray[chosenDoor], (i, doorArray[chosenDoor][1])
                    
        return False
        
    def PrintMap (self):
        
        for row in range(0, self.lvlHeight, 1):
            outputLine = ""
            for col in range(0, self.lvlWidth, 1):
            
                outputLine += str( self.GetMapTile((row, col)) ) + ", "
                
            # print outputLine
            
    def DrawMap (self, thisGame):
        
        self.powerPelletBlinkTimer += 1
        if self.powerPelletBlinkTimer == 60:
            self.powerPelletBlinkTimer = 0
        
        for row in range(-1, thisGame.screenTileSize[0] +1, 1):
            outputLine = ""
            for col in range(-1, thisGame.screenTileSize[1] +1, 1):

                # row containing tile that actually goes here
                actualRow = thisGame.screenNearestTilePos[0] + row
                actualCol = thisGame.screenNearestTilePos[1] + col

                useTile = self.GetMapTile((actualRow, actualCol))
                if not useTile == 0 and not useTile == tileID['door-h'] and not useTile == tileID['door-v']:
                    # if this isn't a blank tile

                    if useTile == tileID['pellet-power']:
                        if self.powerPelletBlinkTimer < 30:
                            screen.blit (tileIDImage[ useTile ], (col * TILE_WIDTH - thisGame.screenPixelOffset[0], row * TILE_HEIGHT - thisGame.screenPixelOffset[1]) )

                    elif useTile == tileID['showlogo']:
                        screen.blit (thisGame.imLogo, (col * TILE_WIDTH - thisGame.screenPixelOffset[0], row * TILE_HEIGHT - thisGame.screenPixelOffset[1]) )
                    
                    elif useTile == tileID['hiscores']:
                            screen.blit(thisGame.imHiscores,(col*TILE_WIDTH-thisGame.screenPixelOffset[0],row*TILE_HEIGHT-thisGame.screenPixelOffset[1]))
                    
                    else:
                        screen.blit (tileIDImage[ useTile ], (col * TILE_WIDTH - thisGame.screenPixelOffset[0], row * TILE_HEIGHT - thisGame.screenPixelOffset[1]) )
        

    def LoadLevel (self, levelNum):
        
        self.map = {}
        
        self.pellets = 0
        
        f = open(os.path.join(SCRIPT_PATH,"res","levels",str(levelNum) + ".txt"), 'r')
        lineNum=-1
        rowNum = 0
        useLine = False
        isReadingLevelData = False
          
        for line in f:

            lineNum += 1

            # print " ------- Level Line " + str(lineNum) + " -------- "
            while len(line)>0 and (line[-1]=="\n" or line[-1]=="\r"): line=line[:-1]
            while len(line)>0 and (line[0]=="\n" or line[0]=="\r"): line=line[1:]
            str_splitBySpace = line.split(' ')


            j = str_splitBySpace[0]
                
            if (j == "'" or j == ""):
                # comment / whitespace line
                # print " ignoring comment line.. "
                useLine = False
            elif j == "#":
                # special divider / attribute line
                useLine = False
                
                firstWord = str_splitBySpace[1]
                
                if firstWord == "lvlwidth":
                    self.lvlWidth = int( str_splitBySpace[2] )
                    # print "Width is " + str( self.lvlWidth )
                    
                elif firstWord == "lvlheight":
                    self.lvlHeight = int( str_splitBySpace[2] )
                    # print "Height is " + str( self.lvlHeight )
                    
                elif firstWord == "edgecolor":
                    # edge color keyword for backwards compatibility (single edge color) mazes
                    red = int( str_splitBySpace[2] )
                    green = int( str_splitBySpace[3] )
                    blue = int( str_splitBySpace[4] )
                    self.edgeLightColor = (red, green, blue, 255)
                    self.edgeShadowColor = (red, green, blue, 255)
                    
                elif firstWord == "edgelightcolor":
                    red = int( str_splitBySpace[2] )
                    green = int( str_splitBySpace[3] )
                    blue = int( str_splitBySpace[4] )
                    self.edgeLightColor = (red, green, blue, 255)
                    
                elif firstWord == "edgeshadowcolor":
                    red = int( str_splitBySpace[2] )
                    green = int( str_splitBySpace[3] )
                    blue = int( str_splitBySpace[4] )
                    self.edgeShadowColor = (red, green, blue, 255)
                
                elif firstWord == "fillcolor":
                    red = int( str_splitBySpace[2] )
                    green = int( str_splitBySpace[3] )
                    blue = int( str_splitBySpace[4] )
                    self.fillColor = (red, green, blue, 255)
                    
                elif firstWord == "pelletcolor":
                    red = int( str_splitBySpace[2] )
                    green = int( str_splitBySpace[3] )
                    blue = int( str_splitBySpace[4] )
                    self.pelletColor = (red, green, blue, 255)
                    
                elif firstWord == "fruittype":
                    self.thisFruit.fruitType = int( str_splitBySpace[2] )
                    
                elif firstWord == "startleveldata":
                    isReadingLevelData = True
                        # print "Level data has begun"
                    rowNum = 0
                    
                elif firstWord == "endleveldata":
                    isReadingLevelData = False
                    # print "Level data has ended"
                    
            else:
                useLine = True
                
                
            # this is a map data line   
            if useLine == True:
                
                if isReadingLevelData == True:
                        
                    # print str( len(str_splitBySpace) ) + " tiles in this column"
                    
                    for k in range(0, self.lvlWidth, 1):
                        self.SetMapTile((rowNum, k), int(str_splitBySpace[k]) )
                        
                        thisID = int(str_splitBySpace[k])
                        if thisID == 4: 
                            # starting position for pac-man
                            
                            self.player.homeX = k * TILE_WIDTH
                            self.player.homeY = rowNum * TILE_HEIGHT
                            self.SetMapTile((rowNum, k), 0 )
                            
                        elif thisID >= 10 and thisID <= 13:
                            # one of the ghosts
                            
                            self.ghosts[thisID - 10].homeX = k * TILE_WIDTH
                            self.ghosts[thisID - 10].homeY = rowNum * TILE_HEIGHT
                            self.SetMapTile((rowNum, k), 0 )
                        
                        elif thisID == 2:
                            # pellet
                            
                            self.pellets += 1
                            
                    rowNum += 1
                    
                
        # reload all tiles and set appropriate colors
        self.GetCrossRef()

        # load map into the pathfinder object
        self.path.ResizeMap( (self.lvlHeight, self.lvlWidth) )
        
        for row in range(0, self.path.size[0], 1):
            for col in range(0, self.path.size[1], 1):
                if self.IsWall( (row, col) ):
                    self.path.SetType( (row, col), 1 )
                else:
                    self.path.SetType( (row, col), 0 )
        
        
        

    

    def GetCrossRef (self):

        f = open(os.path.join(SCRIPT_PATH,"res","crossref.txt"), 'r')

        lineNum = 0
        useLine = False

        for i in f.readlines():
            # print " ========= Line " + str(lineNum) + " ============ "
            while len(i)>0 and (i[-1]=='\n' or i[-1]=='\r'): i=i[:-1]
            while len(i)>0 and (i[0]=='\n' or i[0]=='\r'): i=i[1:]
            str_splitBySpace = i.split(' ')
            
            j = str_splitBySpace[0]
                
            if (j == "'" or j == "" or j == "#"):
                # comment / whitespace line
                # print " ignoring comment line.. "
                useLine = False
            else:
                # print str(wordNum) + ". " + j
                
                useLine = True
            
            if useLine == True:
                tileIDName[ int(str_splitBySpace[0]) ] = str_splitBySpace[1]
                tileID[ str_splitBySpace[1] ] = int(str_splitBySpace[0])
                
                thisID = int(str_splitBySpace[0])
                if not thisID in NO_GIF_TILES:
                    tileIDImage[ thisID ] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles",str_splitBySpace[1] + ".gif")).convert()
                else:
                        tileIDImage[ thisID ] = pygame.Surface((TILE_WIDTH,TILE_HEIGHT))
                
                # change colors in tileIDImage to match maze colors
                for y in range(0, TILE_WIDTH, 1):
                    for x in range(0, TILE_HEIGHT, 1):
                    
                        if tileIDImage[ thisID ].get_at( (x, y) ) == IMG_EDGE_LIGHT_COLOR:
                            # wall edge
                            tileIDImage[ thisID ].set_at( (x, y), self.edgeLightColor )
                            
                        elif tileIDImage[ thisID ].get_at( (x, y) ) == IMG_FILL_COLOR:
                            # wall fill
                            tileIDImage[ thisID ].set_at( (x, y), self.fillColor ) 
                            
                        elif tileIDImage[ thisID ].get_at( (x, y) ) == IMG_EDGE_SHADOW_COLOR:
                            # pellet color
                            tileIDImage[ thisID ].set_at( (x, y), self.edgeShadowColor )   
                            
                        elif tileIDImage[ thisID ].get_at( (x, y) ) == IMG_PELLET_COLOR:
                            # pellet color
                            tileIDImage[ thisID ].set_at( (x, y), self.pelletColor )   
                    
                # print str_splitBySpace[0] + " is married to " + str_splitBySpace[1]
            lineNum += 1
            
            


