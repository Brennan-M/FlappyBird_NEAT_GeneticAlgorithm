import numpy as np
import random
from datetime import datetime
#import tensorflow as tf


class Interface:

    def __init__(self, net_ID, gen_ID, frequency=15):
        self.network_ID = net_ID
        self.generation_ID = gen_ID
        self.fitness = None
        
        random.seed(datetime.now())

        self.frequency = frequency


    def set_fitness(self, fitness):
        self.fitness = fitness


    def mutate(self):
        """
            Simulates a mutation of the weights or nodes of a neural network.
            Since our 'prediction' is simply pulled from a binomial distribution (I think...),
                then our simulated weight is the frequency (self.frequency)
            To mutate, we flip a coin. 
            If Heads, then we increment the frequency up, else decrement.
        """
        coin_flip = np.random.randint(2)

        if coin_flip == 0:
            return self.frequency + 1
        else:
            return self.frequency - 1



    def update(self, player, pipes):
        self.player_top = player.top
        self.player_bottom = player.bottom

        self.pipes_top = pipes.top
        self.pipes_bottom = pipes.bottom
        self.pipes_left = pipes.left
        self.pipes_right = pipes.right


    def predict(self):
        random_output = np.random.randint(self.frequency)
        if random_output == 0:
            return True
        else:
            return False
        



