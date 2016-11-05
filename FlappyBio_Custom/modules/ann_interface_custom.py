import numpy as np
import random, math
from datetime import datetime
import tensorflow as tf
import modules.neural_network as ann

"""
Neural Network Interface Class
-------------------------------

This class made more sense with TensorFlow. This is just the interface between species.py and neural_network.py.

"""


class Interface:

    def __init__(self, net_ID, gen_ID, speciesID, mutations=None, copy=None):
        self.network_ID = net_ID
        self.generation_ID = gen_ID
        self.species_ID = speciesID
        self.fitness = None
        
        random.seed(datetime.now())

        self._init_network_(mutations, copy)


    def _init_network_(self, mutations, copy=None):
        self.input_layer_size = 8
        if mutations:
            init_hidden_layer_size = mutations[-1]
        else:
            random_size = np.random.randint(12) + 4
            init_hidden_layer_size = random_size
        output_layer_size = 1

        topology = [self.input_layer_size, init_hidden_layer_size, output_layer_size]
        self.network = ann.Network(topology, mutations, copy)
        

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
        output = self.network.output
        return output
        
        



