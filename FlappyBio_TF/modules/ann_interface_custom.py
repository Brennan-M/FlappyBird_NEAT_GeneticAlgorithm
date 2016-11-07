import numpy as np
import random, math
from datetime import datetime
import tensorflow as tf
import modules.neural_network as ann

"""
Neural Network Interface Class
-------------------------------



"""


class Interface:

    def __init__(self, net_ID, gen_ID, species_ID, parent_fitness=None, copy=False, mutation=None):
        self.network_ID = net_ID
        self.generation_ID = gen_ID
        self.species_ID = species_ID

        self.fitness = None
        
        random.seed(datetime.now())

        self.input_layer_size = 8
        self.output_layer_size = 1
        self.topology = [self.input_layer_size, self.output_layer_size]

        self._init_network_(parent_fitness, copy, mutation)


    def _init_network_(self, parent_fitness, copy, mutation):
        
        self.network = ann.Network(self.topology, parent_fitness, copy, mutation)
        

    def set_fitness(self, fitness):
        self.fitness = fitness
        self.network.set_fitness(fitness)


    def mutate(self):

        return self.network.mutate()


    def update(self, player, Upipes, Lpipes):
        
        X = np.zeros(self.input_layer_size)
        X[0] = player.top
        X[1] = player.bottom
        X[2] = player.left
        X[3] = player.right

        X[4] = Upipes.bottom
        X[5] = Lpipes.top
        X[6] = Upipes.left
        X[7] = Upipes.right

        self.network.feed_forward(X)


    def predict(self):
        return self.network.output
        
        



