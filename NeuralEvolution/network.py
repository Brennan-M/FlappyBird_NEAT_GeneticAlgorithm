from NeuralEvolution.neuron import Neuron
from NeuralEvolution.gene import Gene
from copy import deepcopy
import numpy as np
import math
from sklearn import preprocessing



class Network(object):


    def __init__(self, topology, innovation):

        # Neural Net meta data
        self.species_number = None
        self.generation_number = None
        self.fitness = 0

        # Neural Net structure information
        self.num_input_neurons = topology[0]
        self.num_output_neurons = topology[1]

        self.current_neuron_id = 0
        self.innovation = innovation
        
        # Neural Net nodes and edges
        self.genes = {}
        self.neurons = {}

        # Create Neurons
        i = 0
        self.input_neurons = []
        while i < self.num_input_neurons:
            self.neurons[self.current_neuron_id] = Neuron(self.current_neuron_id, "Input")
            self.input_neurons.append(self.neurons[self.current_neuron_id])
            self.current_neuron_id += 1
            i += 1

        i = 0
        self.output_neurons = []
        while i < self.num_output_neurons:
            self.neurons[self.current_neuron_id] = Neuron(self.current_neuron_id, "Output")
            self.output_neurons.append(self.neurons[self.current_neuron_id])
            self.current_neuron_id += 1
            i += 1

        # Create Genes
        for input_neuron in self.input_neurons:
            for output_neuron in self.output_neurons:
                innov_num = self.innovation.get_new_innovation_number()
                self.genes[innov_num] = Gene(innov_num, input_neuron, output_neuron)


    def set_fitness(self, fitness):
        self.fitness = fitness


    def set_generation(self, gen_id):
        self.generation_number = gen_id


    def set_species(self, s_id):
        self.species_number = s_id


    def predict(self, X):
        X = preprocessing.scale(X)

        for i, input_value in enumerate(X):
            self.input_neurons[i].add_input(input_value)

        complete = False
        while not complete:
            complete = True

            for n_id, neuron in self.neurons.items():
                if neuron.ready():
                    for gene in neuron.output_genes.values():
                        if gene.enabled:
                            value = neuron.activation() * gene.weight
                        else:
                            value = 0
                        gene.output_neuron.add_input(value)

                # If the neuron has not yet fired, feed forward it not finished
                if not neuron.sent_output:
                    complete = False

        # This code portion is indeed specific to FlappyBird
        output_neuron = self.output_neurons[0]
        output_value = output_neuron.activation()

        self.reset_neurons()

        return True if output_value >= 0.5 else False


    def reset_neurons(self):
        for n_id, neuron in self.neurons.items():
            neuron.reset_neuron()


    def clone(self):
        return deepcopy(self)


    def reinitialize(self):
        for g_id, gene in self.genes.items():
            gene.randomize_weight()


    # def mutate(self):
    #     pass
    #     # mutation_actions = [self.mutate_W, self.mutate_b]
    #     # action_index = np.random.randint(2)
        
    #     # mutation_actions[action_index]()

        
    # def mutate_W(self, mutation_count=2):

    #     for i in range(mutation_count):
    #         # Declare new mutation sign and magnitude
    #         weight_mutation_direction = np.random.choice(np.asarray([-1, 1]))
    #         weight_mutation_magnitude = np.random.uniform(0, 1)

    #         if (self.structure_type == PERCEPTRON):
    #             # In the future, we will generate 2 random indices, since we will choose a layer as well
    #             weight_index_to_mutate = np.random.randint(self.W.shape[0])

    #             # Apply the mutation
    #             self.W[weight_index_to_mutate] += weight_mutation_direction * weight_mutation_magnitude

    #         else:
    #             if (self.structure_type == NET):
    #                 layers = [self.inputW, self.outputW]
    #             elif (self.structure_type == DEEP_NET):
    #                 layers = [self.inputW, self.W, self.outputW]

    #             layer_index_to_mutate = np.random.randint(len(layers))

    #             weight_col_to_mutate = np.random.randint(layers[layer_index_to_mutate].shape[0])
    #             weight_row_to_mutate = np.random.randint(layers[layer_index_to_mutate].shape[1])

    #             layers[layer_index_to_mutate][weight_col_to_mutate, weight_row_to_mutate] += \
    #                                           weight_mutation_direction * weight_mutation_magnitude
                

    # def mutate_b(self):
    #     # Declare new mutation sign and mangnitude
    #     bias_index_to_mutate = np.random.randint(self.b.shape[0])
    #     bias_mutation_direction = np.random.choice(np.asarray([-1, 1]))
    #     bias_mutation_magnitude = np.random.uniform(0, 1)

    #     self.b[bias_index_to_mutate] += bias_mutation_direction * bias_mutation_magnitude

