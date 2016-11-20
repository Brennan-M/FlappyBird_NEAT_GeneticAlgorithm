RANDOM_PIPES = True
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

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'FlapPyBird/assets/sprites/redbird-upflap.png',
        'FlapPyBird/assets/sprites/redbird-midflap.png',
        'FlapPyBird/assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        'FlapPyBird/assets/sprites/bluebird-upflap.png',
        'FlapPyBird/assets/sprites/bluebird-midflap.png',
        'FlapPyBird/assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'FlapPyBird/assets/sprites/yellowbird-upflap.png',
        'FlapPyBird/assets/sprites/yellowbird-midflap.png',
        'FlapPyBird/assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'FlapPyBird/assets/sprites/background-day.png',
    'FlapPyBird/assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'FlapPyBird/assets/sprites/pipe-green.png',
    'FlapPyBird/assets/sprites/pipe-red.png',
)
