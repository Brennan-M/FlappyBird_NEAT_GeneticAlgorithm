import numpy as np
from sklearn.preprocessing import normalize
#from modules.neuron import *


class Network:

    def __init__(self, topology, mutations=None, copy=None):
        
        self.topology = topology
        
        self.in_layer_size = topology[0]
        self.hidden_layer_size = topology[1]
        self.out_layer_size = topology[2]   

        if copy:
            print("Copy: {}".format(copy))
            self.W1 = copy.network.W1
            self.W2 = copy.network.W2
            self.b1 = copy.network.b1
            self.b2 = copy.network.b2

        elif mutations:
            self.W1 = mutations[0]
            self.W2 = mutations[1]
            self.b1 = mutations[2]
            self.b2 = mutations[3]
            self.hidden_layer_size = mutations[-1]

        else:
            self.W1 = np.random.randn(self.hidden_layer_size, self.in_layer_size)
            self.W2 = np.random.randn(self.out_layer_size, self.hidden_layer_size)
            self.b1 = 0
            self.b2 = 0

        self.output = True


    def feed_forward(self, X):

        # Normalize Input
        norm1 = X / np.linalg.norm(X)
        X_norm = normalize(X[:,np.newaxis], axis=0).ravel()
        
        # Feed forward
        Z1 = np.dot(self.W1, X_norm)
        Z1 = self.softmax(Z1)
        Z2 = np.dot(self.W2, Z1)
        
        self.output = Z2



    def softmax(self, Z):
        soft_max = []
        for z in Z:
            numerator = np.exp(z)
            denom = np.sum(np.exp(Z))
            term = numerator / denom
            soft_max.append(term)
        return soft_max
            

    def mutate(self):
        
        new_b1 = self.b1
        new_b2 = self.b2

        new_hidden_layer_size = self.hidden_layer_size
        if self.chance_mutation():
            mut_factor = self.get_sign_mutation()
            new_hidden_layer_size += mut_factor

            # Generate new W1 and W2 of proper dimension
            # W1
            new_W1 = np.zeros(new_hidden_layer_size, self.in_layer_size)
            for i in range(self.hidden_layer_size):
                for j in range(self.in_layer_size):
                    new_W1[i][j] = self.W1[i][j]


            # W2
            new_W2 = np.zeros(self.out_layer_size, new_hidden_layer_size)
            for i in range(self.out_layer_size):
                for j in range(self.hidden_layer_size):
                    new_W2[i][j] = self.W1[i][j]

        # If hidden layer changes, other matrices cannot stay the same dimensions.
        else:
            new_W1 = self.W1
            new_W2 = self.W2
            if self.chance_mutation():
                mut_factor = np.random.randn(self.hidden_layer_size, self.in_layer_size)
                new_W1 += mut_factor
            
        
            if self.chance_mutation():
                mut_factor = np.random.randn(self.out_layer_size, self.hidden_layer_size)
                new_W2 += mut_factor
            
        
        if self.chance_mutation():
            mut_factor = self.get_sign_mutation() * np.random.randn(1)
            new_b1 += mut_factor
            
        
        if self.chance_mutation():
            mut_factor = self.get_sign_mutation() * np.random.randn(1)
            new_b2 += mut_factor

        
        
        return (new_W1, new_W2, new_b1, new_b2, new_hidden_layer_size)


    def chance_mutation(self):
        mutation_chance = np.random.randint(4)
        if mutation_chance == 0:
            return 0
        else:
            return 1

    def get_sign_mutation(self):
        mutation = np.random.randint(2)
        if mutation == 0:
            return 1
        else:
            return -1






class Neuron:

    def __init__(self):
        pass