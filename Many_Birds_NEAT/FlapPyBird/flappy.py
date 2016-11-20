import random, sys, os, pygame
import numpy as np

from pygame.locals import *
from FlapPyBird.resources.config import *
import FlapPyBird.resources.config_tools as tools
import FlapPyBird.resources.display_tools as disp_tools
from FlapPyBird.modules.flappybird import Bird
from FlapPyBird.modules.pipes import Pipe, Pipes
from FlapPyBird.modules.base import Base


class FlappyBirdApp(object):

    def __init__(self, neural_networks):
        global SCREEN, FPSCLOCK

        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption('Flappy Bird')

        self.score = 0
        self.crash_info = []

        """  CREATE PLAYER """
        self.movementInfo = tools.load_and_initialize()
        self.birds = [Bird(self.movementInfo, neural_network) for neural_network in neural_networks]

        """ CREATE PIPES """
        self.pipes = Pipes(Pipe(), Pipe())

        """ CREATE BASE """
        self.base = Base(self.movementInfo['basex'])


    def play(self):

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            if self.on_loop():
                return
            else:
                self.on_render()



    def on_loop(self):

        # =========----==========================================================
        """ CHECK FLAP """              # NEURAL NET WILL INTERFACE HERE
        # =========----==========================================================
        for bird in self.birds:
            bird.flap_decision(self.pipes)
        # =========----==========================================================



        # =========----==========================================================
        """ CHECK CRASH """
        # =========----==========================================================
        for index, bird in enumerate(self.birds):
            if bird.check_crash(self.pipes, self.base.basex, self.score):
                self.crash_info.append(bird.crashInfo)
                del self.birds[index]
                if len(self.birds) == 0:
                    return True
        # =========----==========================================================


        # =========----==========================================================
        """ CHECK FOR SCORE """
        # =========----==========================================================
        break_one = break_two = False
        for bird in self.birds:
            playerMidPos = bird.x + IMAGES['player'][0].get_width() / 2
            for pipe in self.pipes.upper:
                pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    self.score += 1
                    break_one = break_two = True
                    SOUNDS['point'].play() if SOUND_ON else None
                if break_one:
                    break
            if break_two:
                break

        # =========----==========================================================


        # =========----==========================================================
        """ MOVE BASE """
        # =========----==========================================================
        self.base.move(self.birds)
        # =========----==========================================================


        # =========----==========================================================
        """ MOVE PLAYER """
        # =========----==========================================================
        for bird in self.birds:
            bird.move()
        # =========----==========================================================


        # =========----==========================================================
        """ MOVE PIPES """
        # =========----==========================================================
        self.pipes.move(self.birds)
        # =========----==========================================================
        return False


    def on_render(self):
        # =========----==========================================================
        """ DRAW BACKGROUND """
        # =========----==========================================================
        SCREEN.blit(IMAGES['background'], (0,0))
        # =========----==========================================================


        # =========----==========================================================
        """ DRAW PIPES """
        # =========----==========================================================
        self.pipes.draw(SCREEN)
        # =========----==========================================================


        # =========----==========================================================
        """ DRAW BASE """
        # =========----==========================================================
        SCREEN.blit(IMAGES['base'], (self.base.basex, BASEY))
        # =========----==========================================================


        # =========----==========================================================
        """ DRAW STATS """
        # =========----==========================================================
        disp_tools.displayStat(SCREEN, self.birds[0].distance*-1, text="distance")
        disp_tools.displayStat(SCREEN, self.score, text="scores")
        for bird in self.birds:
            # disp_tools.displayStat(SCREEN, bird.energy_used, text="energy")
            # disp_tools.displayStat(SCREEN, neural_network.topology, text="topology")
            # disp_tools.displayStat(SCREEN, neural_network.species_number, text="species")
            # disp_tools.displayStat(SCREEN, neural_network.generation_number, text="generation")
            SCREEN.blit(IMAGES['player'][bird.index], (bird.x, bird.y))
        # =========----==========================================================


        # =========----==========================================================
        """ UPDATE DISPLAY """
        # =========----==========================================================
        pygame.display.update()
        # =========----==========================================================


        # =========----==========================================================
        """ TICK CLOCK """
        # =========----==========================================================
        FPSCLOCK.tick(FPS)
        # =========----==========================================================


if __name__ == "__main__":
    flappy = FlappyBirdApp()
    flappy.play()
