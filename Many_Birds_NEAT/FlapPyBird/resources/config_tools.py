from FlapPyBird.resources.config import *
import pygame, random
from itertools import cycle

def load_images():
    # numbers sprites for score display
    IMAGES['numbers'] = tuple([pygame.image.load('FlapPyBird/assets/sprites/{}.png'.format(x)).convert_alpha() for x in range(10)])

    sprite_load_list = ["gameover", "message", "base", "energy", "distance",
                        "organism", "generation", "scores", "species", "topology"]

    for sprite in sprite_load_list:
        IMAGES[sprite] = pygame.image.load('FlapPyBird/assets/sprites/{}.png'.format(sprite)).convert_alpha()



def load_sounds():
    if SOUND_ON:
        soundExt = '.wav' if 'win' in sys.platform else '.ogg'
        sound_list = ["die", "hit", "point", "swoosh", "wing"]
        for sound in sound_list:
            SOUNDS[sound] = pygame.mixer.Sound('FlapPyBird/assets/audio/{}'.format(sound) + soundExt)



def initialize_random_sprites():
    # select random background sprites
    randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
    IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

    # select random player sprites
    randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
    IMAGES['player'] = tuple([pygame.image.load(PLAYERS_LIST[randPlayer][i]).convert_alpha() for i in range(3)])

    # select random pipe sprites
    random.seed() if (RANDOM_PIPES) else random.seed(5)

    pipeindex = random.randint(0, len(PIPES_LIST) - 1)
    IMAGES['pipe'] = (
        pygame.transform.rotate(
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
        pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
    )

    


def initialize_hitmasks():
    # hismask for pipes
    HITMASKS['pipe'] = (getHitmask(IMAGES['pipe'][0]),
                        getHitmask(IMAGES['pipe'][1]),)

    # hitmask for player
    HITMASKS['player'] = (getHitmask(IMAGES['player'][0]),
                          getHitmask(IMAGES['player'][1]),
                          getHitmask(IMAGES['player'][2]),)


def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

def initialize_movement_info():
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

    # make first flap sound and return values for mainGame
    SOUNDS['wing'].play() if SOUND_ON else None
    return {'playery': playery + playerShmVals['val'],
            'basex': basex,
            'playerIndexGen': playerIndexGen,}


def load_and_initialize():
    load_images()
    load_sounds()
    initialize_random_sprites()
    initialize_hitmasks()

    BASESHIFT[0] = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    return initialize_movement_info()
