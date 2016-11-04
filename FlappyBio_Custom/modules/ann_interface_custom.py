import numpy as np
import random, math
from datetime import datetime
import tensorflow as tf
import modules.neural_network as ann

class Interface:

    def __init__(self, net_ID, gen_ID, mutations=None, copy=None):
        self.network_ID = net_ID
        self.generation_ID = gen_ID
        self.fitness = None
        
        random.seed(datetime.now())


        # Set up tensor flow
        self._init_network_(mutations, copy)


    def _init_network_(self, mutations, copy=None):
        """
            What a mess...
        """
        input_layer_size = 6
        if mutations:
            init_hidden_layer_size = mutations[-1]
        else:
            init_hidden_layer_size = 10
        output_layer_size = 1

        topology = [input_layer_size, init_hidden_layer_size, output_layer_size]
        self.network = ann.Network(topology, mutations, copy)
        



    def set_fitness(self, fitness):
        self.fitness = fitness


    def mutate(self):
        """
            Simulates a mutation of the weights or nodes of a neural network.
            Since our 'prediction' is simply pulled from a binomial distribution (I think...),
                then our simulated weight is the frequency (self.frequency)
            To mutate, we roll a 3-sided die. 
                If 0, increment the frequency by 1,
                elif 1, decrement by 1
                else, no mutation.
        """
        return self.network.mutate()




    def update(self, player, pipes):
        
        X = np.zeros(6)
        X[0] = player.top
        X[1] = player.bottom
        X[2] = pipes.top
        X[3] = pipes.bottom
        X[4] = pipes.left
        X[5] = pipes.right

        self.network.feed_forward(X)


 

    def predict(self):
        output = self.network.output
        #print("Output: {}".format(output))
        if output >= 0:
            return True
        else:
            return False
        



