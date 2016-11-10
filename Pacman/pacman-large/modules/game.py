import pygame, sys, os, random
from modules.utilities import *
from modules.settings import *

class game ():

    def __init__ (self, path, player, ghosts, thisFruit, thisLevel, ann_feed):
        self.levelNum = 0
        self.score = 0
        self.lives = 3

        self.player = player
        self.path = path
        self.ghosts = ghosts
        self.thisFruit = thisFruit
        self.thisLevel = thisLevel
        self.ann_feed = ann_feed
        

        # game "mode" variable
        # 1 = normal
        # 2 = hit ghost
        # 3 = game over
        # 4 = wait to start
        # 5 = wait after eating ghost
        # 6 = wait after finishing level
        self.mode = 0
        self.modeTimer = 0
        self.ghostTimer = 0
        self.ghostValue = 0
        self.fruitTimer = 0
        self.fruitScoreTimer = 0
        self.fruitScorePos = (0, 0)
        
        self.SetMode( 3 )
        


        # camera variables
        self.screenPixelPos = (0, 0) # absolute x,y position of the screen from the upper-left corner of the level
        self.screenNearestTilePos = (0, 0) # nearest-tile position of the screen from the UL corner
        self.screenPixelOffset = (0, 0) # offset in pixels of the screen from its nearest-tile position
        
        self.screenTileSize = (23, 21)
        self.screenSize = (self.screenTileSize[1] * TILE_WIDTH, self.screenTileSize[0] * TILE_HEIGHT)
        


        # numerical display digits
        self.digit = {}
        for i in range(0, 10, 1):
            self.digit[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","text",str(i) + ".gif")).convert()
        self.imLife = pygame.image.load(os.path.join(SCRIPT_PATH,"res","text","life.gif")).convert()
        self.imGameOver = pygame.image.load(os.path.join(SCRIPT_PATH,"res","text","gameover.gif")).convert()
        self.imReady = pygame.image.load(os.path.join(SCRIPT_PATH,"res","text","ready.gif")).convert()
        self.imLogo = pygame.image.load(os.path.join(SCRIPT_PATH,"res","text","logo.gif")).convert()
        self.imHiscores = self.makehiscorelist()



    def defaulthiscorelist(self):
            return [ (100000,"David") , (80000,"Andy") , (60000,"Count Pacula") , (40000,"Cleopacra") , (20000,"Brett Favre") , (10000,"Sergei Pachmaninoff") ]


    def gethiscores(self):
            """If res/hiscore.txt exists, read it. If not, return the default high scores.
               Output is [ (score,name) , (score,name) , .. ]. Always 6 entries."""
            try:
              f=open(os.path.join(SCRIPT_PATH,"res","hiscore.txt"))
              hs=[]
              for line in f:
                while len(line)>0 and (line[0]=="\n" or line[0]=="\r"): line=line[1:]
                while len(line)>0 and (line[-1]=="\n" or line[-1]=="\r"): line=line[:-1]
                score=int(line.split(" ")[0])
                name=line.partition(" ")[2]
                if score>99999999: score=99999999
                if len(name)>22: name=name[:22]
                hs.append((score,name))
              f.close()
              if len(hs)>6: hs=hs[:6]
              while len(hs)<6: hs.append((0,""))
              return hs
            except IOError:
   
              return self.defaulthiscorelist()
              
    def writehiscores(self,hs):
            """Given a new list, write it to the default file."""
            fname=os.path.join(SCRIPT_PATH,"res","hiscore.txt")
            f=open(fname,"w")
            for line in hs:
              f.write(str(line[0])+" "+line[1]+"\n")
            f.close()
   

    def getplayername(self):
            """Ask the player his name, to go on the high-score list."""
            if NO_WX: return USER_NAME
            try:
              import wx
            except:
              print "Pacman Error: No module wx. Can not ask the user his name!"
              print "     :(       Download wx from http://www.wxpython.org/"
              print "     :(       To avoid seeing this error again, set NO_WX in file pacman.pyw."
              return USER_NAME
            app=wx.App(None)
            dlog=wx.TextEntryDialog(None,"You made the high-score list! Name:")
            dlog.ShowModal()
            name=dlog.GetValue()
            dlog.Destroy()
            app.Destroy()
            return name
       

    def updatehiscores(self,newscore):
            """Add newscore to the high score list, if appropriate."""
            hs=self.gethiscores()
            for line in hs:
              if newscore>=line[0]:
                hs.insert(hs.index(line),(newscore,self.getplayername()))
                hs.pop(-1)
                break
            self.writehiscores(hs)


    def makehiscorelist(self):
            "Read the High-Score file and convert it to a useable Surface."
            # My apologies for all the hard-coded constants.... -Andy
            f=pygame.font.Font(os.path.join(SCRIPT_PATH,"res","VeraMoBd.ttf"),HS_FONT_SIZE)
            scoresurf=pygame.Surface((HS_WIDTH,HS_HEIGHT),pygame.SRCALPHA)
            scoresurf.set_alpha(HS_ALPHA)
            linesurf=f.render(" "*18+"HIGH SCORES",1,(255,255,0))
            scoresurf.blit(linesurf,(0,0))
            hs=self.gethiscores()
            vpos=0
            for line in hs:
              vpos+=HS_LINE_HEIGHT
              linesurf=f.render(line[1].rjust(22)+str(line[0]).rjust(9),1,(255,255,255))
              scoresurf.blit(linesurf,(0,vpos))
            return scoresurf
            
    def drawmidgamehiscores(self):
            """Redraw the high-score list image after pacman dies."""
            self.imHiscores=self.makehiscorelist()



    def RestartLevel(self):
        for i in range(0, 4, 1):
            # move ghosts back to home

            self.ghosts[i].x = self.ghosts[i].homeX
            self.ghosts[i].y = self.ghosts[i].homeY
            self.ghosts[i].velX = 0
            self.ghosts[i].velY = 0
            self.ghosts[i].state = 1
            self.ghosts[i].speed = 1
            self.ghosts[i].Move(self.player, self.thisLevel)
            
            # give each ghost a path to a random spot (containing a pellet)
            (randRow, randCol) = (0, 0)

            while not self.thisLevel.GetMapTile((randRow, randCol)) == tileID[ 'pellet' ] or (randRow, randCol) == (0, 0):
                randRow = random.randint(1, self.thisLevel.lvlHeight - 2)
                randCol = random.randint(1, self.thisLevel.lvlWidth - 2)
            
            # print "Ghost " + str(i) + " headed towards " + str((randRow, randCol))
            self.ghosts[i].currentPath = self.path.FindPath( (self.ghosts[i].nearestRow, self.ghosts[i].nearestCol), (randRow, randCol) )
            self.ghosts[i].FollowNextPathWay(self.player, self.thisLevel)
            
        self.thisFruit.active = False
            
        self.fruitTimer = 0

        self.player.x = self.player.homeX
        self.player.y = self.player.homeY
        self.player.velX = 0
        self.player.velY = 0
        
        self.player.anim_pacmanCurrent = self.player.anim_pacmanS
        self.player.animFrame = 3



    def StartNewGame (self):
        self.levelNum = 1
        self.score = 0
        self.lives = 3

        self.SetMode( 4 )
        self.thisLevel.LoadLevel(self.GetLevelNum())
        self.RestartLevel()

    def AddToScore (self, amount):

        extraLifeSet = [25000, 50000, 100000, 150000]

        for specialScore in extraLifeSet:
            if self.score < specialScore and self.score + amount >= specialScore:
                #snd_extralife.play()
                self.lives += 1

        self.score += amount


    def DrawScore (self):
        self.DrawNumber (self.score, (SCORE_XOFFSET, self.screenSize[1] - SCORE_YOFFSET) )

        for i in range(0, self.lives, 1):
            screen.blit (self.imLife, (34 + i * 10 + 16, self.screenSize[1] - 18) )

        screen.blit (self.thisFruit.imFruit[ self.thisFruit.fruitType ], (4 + 16, self.screenSize[1] - 28) )

        if self.mode == 3:
            screen.blit (self.imGameOver, (self.screenSize[0] / 2 - (self.imGameOver.get_width()/2), self.screenSize[1] / 2 - (self.imGameOver.get_height()/2)) )
        elif self.mode == 4:
            screen.blit (self.imReady, (self.screenSize[0] / 2 - 20, self.screenSize[1] / 2 + 12) )

        self.DrawNumber (self.levelNum, (0, self.screenSize[1] - 20) )
            
    def DrawNumber (self, number, (x, y)):
        strNumber = str(number)

        for i in range(0, len(str(number)), 1):
            iDigit = int(strNumber[i])
            screen.blit (self.digit[ iDigit ], (x + i * SCORE_COLWIDTH, y) )

    def SmartMoveScreen (self):

        possibleScreenX = self.player.x - self.screenTileSize[1] / 2 * TILE_WIDTH
        possibleScreenY = self.player.y - self.screenTileSize[0] / 2 * TILE_HEIGHT

        if possibleScreenX < 0:
            possibleScreenX = 0
        elif possibleScreenX > self.thisLevel.lvlWidth * TILE_WIDTH - self.screenSize[0]:
            possibleScreenX = self.thisLevel.lvlWidth * TILE_HEIGHT - self.screenSize[0]

        if possibleScreenY < 0:
            possibleScreenY = 0
        elif possibleScreenY > self.thisLevel.lvlHeight * TILE_WIDTH - self.screenSize[1]:
            possibleScreenY = self.thisLevel.lvlHeight * TILE_HEIGHT - self.screenSize[1]

        self.MoveScreen( (possibleScreenX, possibleScreenY) )
        
    def MoveScreen (self, (newX, newY) ):
        self.screenPixelPos = (newX, newY)
        self.screenNearestTilePos = (int(newY / TILE_HEIGHT), int(newX / TILE_WIDTH)) # nearest-tile position of the screen from the UL corner
        self.screenPixelOffset = (newX - self.screenNearestTilePos[1]*TILE_WIDTH, newY - self.screenNearestTilePos[0]*TILE_HEIGHT)
        
    def GetScreenPos (self):
        return self.screenPixelPos
        
    def GetLevelNum (self):
        return self.levelNum
    
    def SetNextLevel (self):
        self.levelNum += 1
        
        self.SetMode( 4 )
        self.thisLevel.LoadLevel(self.GetLevelNum())
        self.RestartLevel()

        self.player.velX = 0
        self.player.velY = 0
        self.player.anim_pacmanCurrent = self.player.anim_pacmanS

    def SetMode (self, newMode):
        self.mode = newMode
        self.modeTimer = 0
        # print " ***** GAME MODE IS NOW ***** " + str(newMode)



    def Move(self):
        self.player.Move(self.thisLevel, self.ghosts, self.thisFruit, self)
        for i in range(0, 4, 1):
            self.ghosts[i].Move(self.player, self.thisLevel)
        self.thisFruit.Move(self)



    def Play(self):
        oldEdgeLightColor = self.thisLevel.edgeLightColor
        oldEdgeShadowColor = self.thisLevel.edgeShadowColor
        oldFillColor = self.thisLevel.fillColor

        if self.mode == 1:
            # normal gameplay mode
            CheckInputs(self.player, self, self.thisLevel)
            self.modeTimer += 1
            self.Move()
            
        elif self.mode == 2:
            # waiting after getting hit by a ghost
            self.modeTimer += 1
            
            if self.modeTimer == 90:
                self.RestartLevel()
                
                self.lives -= 1
                if self.lives == -1:
                    self.updatehiscores(self.score)
                    self.SetMode( 3 )
                    self.drawmidgamehiscores()
                else:
                    self.SetMode( 4 )
                 

        elif self.mode == 3:
            # game over
            CheckInputs(self.player, self, self.thisLevel)
                

        elif self.mode == 4:
            # waiting to start
            self.modeTimer += 1
            
            if self.modeTimer == 90:
                self.SetMode( 1 )
                self.player.velX = self.player.speed
                

        elif self.mode == 5:
            # brief pause after munching a vulnerable ghost
            self.modeTimer += 1
            
            if self.modeTimer == 30:
                self.SetMode( 1 )
                
        elif self.mode == 6:
            # pause after eating all the pellets
            self.modeTimer += 1
            
            if self.modeTimer == 60:
                self.SetMode( 7 )
                oldEdgeLightColor = self.thisLevel.edgeLightColor
                oldEdgeShadowColor = self.thisLevel.edgeShadowColor
                oldFillColor = self.thisLevel.fillColor
                
        elif self.mode == 7:
            # flashing maze after finishing level
            self.modeTimer += 1
            
            whiteSet = [10, 30, 50, 70]
            normalSet = [20, 40, 60, 80]
            
            if not whiteSet.count(self.modeTimer) == 0:
                # member of white set
                self.thisLevel.edgeLightColor = (255, 255, 254,255)
                self.thisLevel.edgeShadowColor = (255, 255, 254,255)
                self.thisLevel.fillColor = (0, 0, 0,255)
                self.thisLevel.GetCrossRef()
            elif not normalSet.count(self.modeTimer) == 0:
                # member of normal set
                self.thisLevel.edgeLightColor = oldEdgeLightColor
                self.thisLevel.edgeShadowColor = oldEdgeShadowColor
                self.thisLevel.fillColor = oldFillColor
                self.thisLevel.GetCrossRef()
            elif self.modeTimer == 150:
                self.SetMode ( 8 )
                
        elif self.mode == 8:
            # blank screen before changing levels
            self.modeTimer += 1
            if self.modeTimer == 10:
                self.SetNextLevel()

        self.SmartMoveScreen()
        
        screen.blit(img_Background, (0, 0))
        
        if not self.mode == 8:
            self.thisLevel.DrawMap(self)
            
            if self.fruitScoreTimer > 0:
                if self.modeTimer % 2 == 0:
                    self.DrawNumber (2500, (self.thisFruit.x - self.screenPixelPos[0] - 16, self.thisFruit.y - self.screenPixelPos[1] + 4))

            for i in range(0, 4, 1):
                self.ghosts[i].Draw(self, self.player, self.ghosts)
            self.thisFruit.Draw(self)
            self.player.Draw(self)
            
            if self.mode == 3:
                    screen.blit(self.imHiscores,(HS_XOFFSET,HS_YOFFSET))
            
        if self.mode == 5:
            self.DrawNumber (self.ghostValue / 2, (self.player.x - self.screenPixelPos[0] - 4, self.player.y - self.screenPixelPos[1] + 6))
        

        self.ann_feed.update(self.player, self.ghosts, self.thisFruit, self.thisLevel.map)
        
        self.DrawScore()
        
        pygame.display.flip()
        
        clock.tick (60)
    
    def LoadLevel(self):
        self.thisLevel.LoadLevel(self.GetLevelNum())
        self.RestartLevel()
      