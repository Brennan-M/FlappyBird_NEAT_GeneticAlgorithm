import numpy as np
import math
from sklearn import preprocessing


def mate(parent_A, parent_B):
    # TODO: More sophisticated genetic engineering. 
    # Currently, chooses the fittest partent's genes
    if parent_A.fitness > parent_B.fitness:
        return parent_A.get_genes()
    else:
        return parent_B.get_genes()

class Network(object):


    def __init__(self, topology, network_info, inherited_genes=None):

        # Neural Net meta data
        self.network_number = network_info["network"]
        self.generation_number = network_info["generation"]
        self.species_number = network_info["species"]

        # Neural Net structure information
        self.topology = topology
        self.num_input_neurons = self.topology[0]
        self.num_output_neurons = self.topology[1]
        self.num_layers = 1 # No hidden layers used currently

        # Neural Net values
        self.fitness = 0
        self.x = np.zeros([1, self.num_input_neurons])

        if (inherited_genes): # Inherit parent genes
            self.W = np.copy(inherited_genes[0])
            self.b = np.copy(inherited_genes[1])
        else:
            self.W = np.random.rand(self.num_input_neurons, self.num_output_neurons)
            self.b = np.random.rand(1, self.num_layers)

        # Any of our activation functions, (sigmoid or relu)
        self.activation = lambda t: 1 if self.relu(t) >= 0.5 else 0

    
    def relu(self, T):
        return math.log(1.0 + math.e**(-T)) # Smooth approximation
        # return max(0, T) # Regular relu


    def sigmoid(self, T):
        return ( 1.0 / (1.0 + math.e**(-T)))
      
        
    def get_genes(self):
        return (self.W, self.b)


    def normalize_vector(self, vect):
        return preprocessing.scale(vect)


    # TODO: Handle multiple layer feed forward (currently a perceptron)
    def predict(self, X, normalize_input=True):
        X = np.asarray(X) 

        if normalize_input:
            X = self.normalize_vector(X)

        return self.activation(self.W.T.dot(X) + self.b)


    def set_fitness(self, fitness):
        self.fitness = fitness


    def mutate(self):
        mutation_actions = [self.mutate_W, self.mutate_b]
        action_index = np.random.randint(2)
        
        mutation_actions[action_index]()

        
    def mutate_W(self):
        # Declare new mutation sign and magnitude
        weight_mutation_direction = np.random.choice(np.asarray([-1, 1]))
        weight_mutation_magnitude = np.random.uniform(0, 1)

        # In the future, we will generate 2 random indices, since we will choose a layer as well
        weight_index_to_mutate = np.random.randint(self.W.shape[0])

        # Apply the mutation
        self.W[weight_index_to_mutate] += weight_mutation_direction * weight_mutation_magnitude


    def mutate_b(self):
        # Declare new mutation sign and mangnitude
        bias_mutation_direction = np.random.choice(np.asarray([-1, 1]))
        bias_mutation_magnitude = np.random.uniform(0, 1)

        self.b += bias_mutation_direction * bias_mutation_magnitude

