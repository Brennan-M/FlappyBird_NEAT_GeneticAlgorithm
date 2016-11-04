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
        self.input_layer_size = 8
        if mutations:
            init_hidden_layer_size = mutations[-1]
        else:
            init_hidden_layer_size = 4
        output_layer_size = 1

        topology = [self.input_layer_size, init_hidden_layer_size, output_layer_size]
        self.network = ann.Network(topology, mutations, copy)
        



    def set_fitness(self, fitness):
        self.fitness = fitness
        self.network.set_fitness(fitness)


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

        
       

        print("\nNN Inputs")
        print("\tPlayer top: {}".format(X[0]))
        print("\tPlayer bottom: {}".format(X[1]))
        print("\tPlayer left: {}".format(X[2]))
        print("\tPipes right: {}".format(X[3]))
        print("\t---------------")
        print("\tUpper Pipes bottom: {}".format(X[4]))
        print("\tLower Pipes top: {}".format(X[5]))
        print("\tPipes left: {}".format(X[6]))
        print("\tPipes right: {}".format(X[7]))
        
        print("\n")
        self.network.feed_forward(X)


 

    def predict(self):
        output = self.network.output
        return output
        
        



