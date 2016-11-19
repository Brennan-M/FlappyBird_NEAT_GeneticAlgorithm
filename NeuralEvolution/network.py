import numpy as np
import math
from sklearn import preprocessing


# Define 3 distinct possible structures for our neural net
PERCEPTRON = 0
NET = 1
DEEP_NET = 2



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
        self.num_hidden_neurons = self.topology[2]
        self.num_hidden_layers = self.topology[3] 
        if (self.num_hidden_layers == 0):
            self.structure_type = PERCEPTRON
        elif (self.num_hidden_layers == 1):
            self.structure_type = NET
        else:
            self.structure_type = DEEP_NET

        # Neural Net values
        self.fitness = 0
        self.x = np.zeros([1, self.num_input_neurons])

        if (inherited_genes): # Inherit parent genetics

            if (self.structure_type == PERCEPTRON):
                self.W = np.copy(inherited_genes[0])
                self.b = np.copy(inherited_genes[1])

            elif (self.structure_type == NET):
                self.inputW = np.copy(inherited_genes[0])
                self.outputW = np.copy(inherited_genes[1])
                self.b = np.copy(inherited_genes[2])

            elif (self.structure_type == DEEP_NET):
                self.inputW = np.copy(inherited_genes[0])
                self.W = np.copy(inherited_genes[1])
                self.outputW = np.copy(inherited_genes[2])
                self.b = np.copy(inherited_genes[3])

        elif (not inherited_genes): # Spawn new genetics

            if (self.structure_type == PERCEPTRON):
                self.W = np.random.rand(self.num_input_neurons)
                self.b = np.random.rand(1, 1)

            elif (self.structure_type == NET):
                self.inputW = np.random.rand(self.num_input_neurons, self.num_hidden_neurons)
                self.outputW = np.random.rand(self.num_hidden_neurons, self.num_output_neurons)
                self.b = np.random.rand(self.num_hidden_layers+1, 1)

            elif (self.structure_type == DEEP_NET):
                self.inputW = np.random.rand(self.num_input_neurons, self.num_hidden_neurons)
                self.W = np.random.rand(self.num_hidden_layers,
                                        self.num_hidden_neurons,
                                        self.num_hidden_neurons)
                self.outputW = np.random.rand(self.num_hidden_neurons, self.num_output_neurons)
                self.b = np.random.rand(self.num_hidden_layers, 1)

        # Any of our activation functions, (sigmoid or relu)
        self.activation = lambda t: 1 if self.relu(t) >= 0.5 else 0

    
    def relu(self, T):
        return math.log(1.0 + math.e**(-T)) # Smooth approximation
        # return max(0, T) # Regular relu


    def sigmoid(self, T):
        return ( 1.0 / (1.0 + math.e**(-T)))
      
        
    def get_genes(self):
        if (self.structure_type == PERCEPTRON):
            return (self.W, self.b)
        elif (self.structure_type == NET):
            return (self.inputW, self.outputW, self.b)
        elif (self.structure_type == DEEP_NET):
            return (self.inputW, self.W, self.outputW, self.b)


    def normalize_vector(self, vect):
        return preprocessing.scale(vect)


    def predict(self, X, normalize_input=True):
        X = np.asarray(X) 

        if normalize_input:
            X = self.normalize_vector(X)

        if (self.structure_type == PERCEPTRON):
            return self.activation(self.W.T.dot(X) + self.b)

        elif (self.structure_type == NET):
            A = [self.activation(self.inputW[:, i].T.dot(X) + self.b[0])
                     for i in range(self.num_hidden_neurons)]
            return self.activation(self.outputW.T.dot(A) + self.b[1])

        elif (self.structure_type == DEEP_NET):
            A = [self.activation(self.inputW[:, i].T.dot(X) + self.b[0])
                     for i in range(self.num_hidden_neurons)]

            for i in range(self.num_hidden_layers-1):
                A = [self.activation(self.W[i, :, j].T.dot(A) + self.b[i+1])
                        for j in range(self.num_hidden_neurons)]

            return self.activation(self.outputW.T.dot(A) + self.b[-1])


    def set_fitness(self, fitness):
        self.fitness = fitness


    def mutate(self):
        mutation_actions = [self.mutate_W, self.mutate_b]
        action_index = np.random.randint(2)
        
        mutation_actions[action_index]()

        
    def mutate_W(self, mutation_count=3):

        for i in range(mutation_count):
            # Declare new mutation sign and magnitude
            weight_mutation_direction = np.random.choice(np.asarray([-1, 1]))
            weight_mutation_magnitude = np.random.uniform(0, 1)

            if (self.structure_type == PERCEPTRON):
                # In the future, we will generate 2 random indices, since we will choose a layer as well
                weight_index_to_mutate = np.random.randint(self.W.shape[0])

                # Apply the mutation
                self.W[weight_index_to_mutate] += weight_mutation_direction * weight_mutation_magnitude

            else:
                if (self.structure_type == NET):
                    layers = [self.inputW, self.outputW]
                elif (self.structure_type == DEEP_NET):
                    layers = [self.inputW, self.W, self.outputW]

                layer_index_to_mutate = np.random.randint(len(layers))

                weight_col_to_mutate = np.random.randint(layers[layer_index_to_mutate].shape[0])
                weight_row_to_mutate = np.random.randint(layers[layer_index_to_mutate].shape[1])

                layers[layer_index_to_mutate][weight_col_to_mutate, weight_row_to_mutate] += \
                                              weight_mutation_direction * weight_mutation_magnitude
                

    def mutate_b(self):
        # Declare new mutation sign and mangnitude
        bias_index_to_mutate = np.random.randint(self.b.shape[0])
        bias_mutation_direction = np.random.choice(np.asarray([-1, 1]))
        bias_mutation_magnitude = np.random.uniform(0, 1)

        self.b[bias_index_to_mutate] += bias_mutation_direction * bias_mutation_magnitude

