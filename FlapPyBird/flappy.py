from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *


RANDOM_PIPES = True


FPS = 60 # Seems I cannot speed it up past this.
SCREENWIDTH  = 288
SCREENHEIGHT = 512
# amount by which base can maximum shift to left
PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)


def main(neural_network):
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha(),
    )

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

    # Energy and Distance display
    IMAGES['energy'] = pygame.image.load('assets/sprites/energy.png').convert_alpha()
    IMAGES['distance'] = pygame.image.load('assets/sprites/distance.png').convert_alpha()

    # Network
    IMAGES['organism'] = pygame.image.load('assets/sprites/organism.png').convert_alpha()
    IMAGES['generation'] = pygame.image.load('assets/sprites/generation.png').convert_alpha()

    # scores display
    IMAGES['scores'] = pygame.image.load('assets/sprites/scores.png').convert_alpha()

    # Species number
    IMAGES['species'] = pygame.image.load('assets/sprites/species.png').convert_alpha()

    # Topology
    IMAGES['topology'] = pygame.image.load('assets/sprites/topology.png').convert_alpha()

    # # Max Score
    # IMAGES['max_score'] = pygame.image.load('assets/sprites/max_score.png').convert_alpha()
    # # Import maxscore
    # with open('assets/max_score.txt', 'r') as infile:
    #     max_score = infile.readline()

    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)

    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )

        # select random pipe sprites
        if (RANDOM_PIPES):
            random.seed()
        else:
            random.seed(5)
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.rotate(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # hismask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask for player
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )

        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo, neural_network)

        return crashInfo


def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""

    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    basex = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player shm for up-down motion on welcome screen
    playerShmVals = {'val': 0, 'dir': 1}

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
        # make first flap sound and return values for mainGame
        SOUNDS['wing'].play()
        return {
            'playery': playery + playerShmVals['val'],
            'basex': basex,
            'playerIndexGen': playerIndexGen,
        }

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
            playerIndex = playerIndexGen.next()
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 4) % baseShift)
        playerShm(playerShmVals)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['player'][playerIndex],
                    (playerx, playery + playerShmVals['val']))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, BASEY))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame(movementInfo, neural_network):

    score = playerIndex = playerDistance = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']


    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    # player velocity, max velocity, downward accleration, accleration on flap
    playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
    playerMaxVelY =  10   # max vel along Y, max descend speed
    playerMinVelY =  -8   # min vel along Y, max ascend speed
    playerAccY    =   1   # players downward accleration
    playerFlapAcc =  -9   # players speed on flapping
    playerFlapped = False # True when player flaps
    playerEnergyUsed = 0

    
    while True:
    
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()


        # Predict Input to Mr. Flappy
        neural_input = [0 for i in range(10)]
        neural_input[0] = float(playerx)
        neural_input[1] = float(playery)
        neural_input[2] = float(upperPipes[0]['y'])
        neural_input[3] = float(upperPipes[0]['x'])
        neural_input[4] = float(upperPipes[1]['y'])
        neural_input[5] = float(upperPipes[1]['x'])
        neural_input[6] = float(lowerPipes[0]['y'])
        neural_input[7] = float(lowerPipes[0]['x'])
        neural_input[8] = float(lowerPipes[1]['y'])
        neural_input[9] = float(lowerPipes[1]['x'])
        # if (len(upperPipes) == 3):
        #     neural_input[10] = float(upperPipes[2]['y'])
        #     neural_input[11] = float(upperPipes[2]['x'])
        #     neural_input[12] = float(lowerPipes[2]['y'])
        #     neural_input[13] = float(lowerPipes[2]['x'])
        # else: 
        #     neural_input[10] = 0
        #     neural_input[11] = 0
        #     neural_input[12] = 0
        #     neural_input[13] = 0
        # If neural_network predicts 1, jump
        if neural_network.predict(neural_input) == 1:
            if playery > -2 * IMAGES['player'][0].get_height():
                playerVelY = playerFlapAcc
                playerFlapped = True
                playerEnergyUsed += 10
                SOUNDS['wing'].play()

        # check for crash here
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                               upperPipes, lowerPipes)


        if crashTest[0]:
            # Values returned to species.py
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
                'distance': playerDistance*-1,
                'energy': playerEnergyUsed
            }

        # check for score
        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                SOUNDS['point'].play()

        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            playerIndex = playerIndexGen.next()
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX
            playerDistance += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        # print score so player overlaps the score
        showScore(score)
        #showMaxScore(max_score)

        # print energy
        showMetric(playerEnergyUsed, text="energy")
        showMetric(playerDistance*-1, text="distance")

        # print network info
        showNetwork(neural_network.network_number, playerDistance*-1, y_position=0.7, text="organism")
        showNetwork(neural_network.generation_number, x_position=0.999, y_position=0.7, text="generation")
        showTopology(neural_network.topology)

        # print species ID:
        showSpeciesID(neural_network.species_number, text="species")



        SCREEN.blit(IMAGES['player'][playerIndex], (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def getRandomPipe():
    """returns a randomly generated pipe"""
    if (RANDOM_PIPES):
        random.seed()
    else:
        random.seed(5)
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]


def showMaxScore(max_score, text="max_score"):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(max_score))]
    totalWidth = 0 # total width of all numbers to be printed

    x_position=0.999
    y_position=0.04

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / x_position

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (40, SCREENHEIGHT * y_position + 10))
        Xoffset += IMAGES['numbers'][digit].get_width()

    SCREEN.blit(IMAGES[text], (0, 0))


def showNetwork(ID, x_position=4, y_position=0.9, text=None):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(ID))]
    
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / x_position

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * y_position + 10))
        Xoffset += IMAGES['numbers'][digit].get_width()

    if text == "organism":
        SCREEN.blit(IMAGES[text], (-8, 395))
    elif text == "generation":
        SCREEN.blit(IMAGES[text], (190, 395))


def showSpeciesID(species, text=None):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(species))]
    totalWidth = 0 # total width of all numbers to be printed

    x_position=0.999
    y_position=0.04

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / x_position

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset-25, SCREENHEIGHT * y_position + 10))
        Xoffset += IMAGES['numbers'][digit].get_width()

    SCREEN.blit(IMAGES[text], (205, 0))
    


def showMetric(stat, text=None):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(stat))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2
    Yoffset = SCREENHEIGHT - 40

    if text == "energy":
        for digit in scoreDigits:
            SCREEN.blit(IMAGES['numbers'][digit], (Xoffset - 70, Yoffset))
            Xoffset += IMAGES['numbers'][digit].get_width()
        SCREEN.blit(IMAGES[text], (35, 440))

    elif text == "distance":
        for digit in scoreDigits:
            SCREEN.blit(IMAGES['numbers'][digit], (Xoffset + 100, Yoffset))
            Xoffset += IMAGES['numbers'][digit].get_width()
        SCREEN.blit(IMAGES[text], (205, 440))


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()

    SCREEN.blit(IMAGES['scores'], (105, 15))

def showTopology(topology, text='topology'):
    """displays score in center of screen"""
    
    text_font = pygame.font.Font(None, 30)

    # Input
    text = text_font.render("I:" + str(topology[0]), 1, (0, 0, 0))
    SCREEN.blit(text, (140, 430))

    # Output
    text = text_font.render("O:" + str(topology[1]), 1, (0, 0, 0))
    SCREEN.blit(text, (140, 450)) 
   
    # -h
    text = text_font.render("H:" + str(topology[2]), 1, (0, 0, 0))
    SCREEN.blit(text, (140, 470)) 

    # -l
    text = text_font.render("L:" + str(topology[3]), 1, (0, 0, 0))
    SCREEN.blit(text, (140, 490))


        
    

    
    SCREEN.blit(IMAGES['topology'], (100, 395))
    

def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]


def pixelCollision(rect1, rect2, hitmask1, hitmask2, display_position=False):
    """Checks if two objects collide and not just their rects"""
    
    if display_position:
        print("Player -- left : {} \t top   : {}".format(rect1.left, rect1.top))
        print("       -- right: {} \t bottom: {}\n".format(rect1.right, rect1.bottom))

        print("Pipes -- left : {} \t top   : {}".format(rect2.left, rect2.top))
        print("       -- right: {} \t bottom: {}\n".format(rect2.right, rect2.bottom))
        print("\n")


    rect = rect1.clip(rect2)
    


    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False


def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

if __name__ == '__main__':
    main()