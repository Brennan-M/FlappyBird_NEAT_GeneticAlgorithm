from FlapPyBird.resources.config import *
import random

class Pipe(object):

    def __init__(self):
        random.seed() if (RANDOM_PIPES) else random.seed(5)

        # y of gap between upper and lower pipe
        gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
        gapY += int(BASEY * 0.2)
        pipeHeight = IMAGES['pipe'][0].get_height()
        pipeX = SCREENWIDTH + 10
        pipeY_upper = gapY - pipeHeight
        pipeY_lower = gapY + PIPEGAPSIZE

        self.x = pipeX
        self.y_upper = pipeY_upper
        self.y_lower = pipeY_lower


    def move_left(self):
        self.x += self.x_velocity

    def get_upper(self):
        return {'x': self.x, 'y': self.y_upper}

    def get_lower(self):
        return {'x': self.x, 'y': self.y_lower}



class Pipes(object):
    def __init__(self, pipe1, pipe2):
        self.movement_velocity = -4
        self.upper1_x = pipe1.x
        self.upper2_x = pipe2.x

        self.upper = [{'x': SCREENWIDTH + 200, 'y': pipe1.y_upper},
                      {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': pipe2.y_upper}]

        self.lower = [{'x': SCREENWIDTH + 200, 'y': pipe1.y_lower},
                      {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': pipe2.y_lower}]

    def move(self, birds):
        for upper_pipe, lower_pipe in zip(self.upper, self.lower):
            upper_pipe['x'] += self.movement_velocity
            lower_pipe['x'] += self.movement_velocity
            for bird in birds:
                bird.distance += self.movement_velocity

        self.update()

    def update(self):
        # add new pipe when first pipe is about to touch left of screen
        if 0 < self.upper[0]['x'] < 5:
            self.add(Pipe())

        # remove first pipe if its out of the screen
        if self.upper[0]['x'] < -IMAGES['pipe'][0].get_width():
            self.remove()


    def add(self, new_pipe):
        """ ADD NEW PIPE """
        newPipe = Pipe()
        self.upper.append(newPipe.get_upper())
        self.lower.append(newPipe.get_lower())

    def remove(self):
        """ REMOVE FINISHED PIPE """
        self.upper.pop(0)
        self.lower.pop(0)

    def draw(self, SCREEN):
        for uPipe, lPipe in zip(self.upper, self.lower):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))
