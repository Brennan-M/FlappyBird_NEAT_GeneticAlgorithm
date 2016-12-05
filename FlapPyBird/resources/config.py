import os

RANDOM_PIPES = False
SOUND_ON = False

FPS = 60 # Seems I cannot speed it up past this.
SCREENWIDTH  = 288
SCREENHEIGHT = 512
BASESHIFT = [0]

# amount by which base can maximum shift to left
PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

PATH = os.getcwd()

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        PATH + '/FlapPyBird/assets/sprites/redbird-upflap.png',
        PATH + '/FlapPyBird/assets/sprites/redbird-midflap.png',
        PATH + '/FlapPyBird/assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        PATH + '/FlapPyBird/assets/sprites/bluebird-upflap.png',
        PATH + '/FlapPyBird/assets/sprites/bluebird-midflap.png',
        PATH + '/FlapPyBird/assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        PATH + '/FlapPyBird/assets/sprites/yellowbird-upflap.png',
        PATH + '/FlapPyBird/assets/sprites/yellowbird-midflap.png',
        PATH + '/FlapPyBird/assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    PATH + '/FlapPyBird/assets/sprites/background-day.png',
    PATH + '/FlapPyBird/assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    PATH + '/FlapPyBird/assets/sprites/pipe-green.png',
    PATH + '/FlapPyBird/assets/sprites/pipe-red.png',
)
