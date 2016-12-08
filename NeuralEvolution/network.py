from NeuralEvolution.neuron import Neuron
from NeuralEvolution.gene import Gene
import NeuralEvolution.config as config
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
        self.hidden_neurons = []

        # Create Neurons
        i = 0
        self.input_neurons = []
        while i < self.num_input_neurons:
            new_neuron_id = self.get_next_neuron_id()
            self.neurons[new_neuron_id] = Neuron(new_neuron_id, "Input")
            self.input_neurons.append(self.neurons[new_neuron_id])
            i += 1

        i = 0
        self.output_neurons = []
        while i < self.num_output_neurons:
            new_neuron_id = self.get_next_neuron_id()
            self.neurons[new_neuron_id] = Neuron(new_neuron_id, "Output")
            self.output_neurons.append(self.neurons[new_neuron_id])
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


    def get_next_neuron_id(self):
        current_id = self.current_neuron_id
        self.current_neuron_id += 1
        return current_id


    def predict(self, X):
        X = preprocessing.scale(X)

        for i, input_value in enumerate(X):
            self.input_neurons[i].add_input(input_value)

        complete = False
        while not complete:
            complete = True

            for n_id, neuron in self.neurons.items():
                # Neuron has received all inputs, send the output onwards    
                if neuron.ready():
                    neuron.fire()

                # If a neuron has not yet fired, feed forward has not finished
                if not neuron.has_fired():
                    complete = False

        # This code portion (next 2 lines) is indeed specific to FlappyBird
        output_neuron = self.output_neurons[0]
        output_value = output_neuron.activation()

        self.reset_neurons()

        return True if output_value >= config.ACTIVATION_THRESHOLD else False


    def reset_neurons(self):
        for n_id, neuron in self.neurons.items():
            neuron.reset_neuron()


    def clone(self):
        return deepcopy(self)


    def reinitialize(self):
        for g_id, gene in self.genes.items():
            gene.randomize_weight()


    def is_compatible(self, comparison_genome):
        normalization_const = max(len(self.genes), len(comparison_genome.genes))
        normalization_const = normalization_const if normalization_const > 20 else 1
        
        num_excess_genes = len(self.get_excess_genes(comparison_genome))
        num_disjoint_genes = len(self.get_disjoint_genes(comparison_genome))
        avg_weight_diff = self.get_avg_weight_difference(comparison_genome)
        compatibility_score = ((num_excess_genes * config.EXCESS_COMPATIBILITY_CONSTANT) /
                                    normalization_const) +\
                              ((num_disjoint_genes * config.DISJOINT_COMPATIBILITY_CONSTANT) /
                                    normalization_const) +\
                              (avg_weight_diff * config.WEIGHT_COMPATIBILITY_CONSTANT)

        compatible = compatibility_score < config.COMPATIBILITY_THRESHOLD
        return compatible


    def get_excess_genes(self, comparison_genome):
        excess_genes = []
        largest_innovation_id = max(self.genes.keys())

        for g_id, genome in comparison_genome.genes.items():
            if g_id > largest_innovation_id:
                excess_genes.append(genome)

        return excess_genes


    def get_disjoint_genes(self, comparison_genome):
        disjoint_genes = []
        largest_innovation_id = max(self.genes.keys())

        for g_id, genome in comparison_genome.genes.items():
            if not self.genes.has_key(g_id) and g_id < largest_innovation_id:
                disjoint_genes.append(genome)

        for g_id, genome in self.genes.items():
            if not comparison_genome.genes.has_key(g_id):
                disjoint_genes.append(genome)

        return disjoint_genes


    def get_avg_weight_difference(self, comparison_genome):
        avg_weight_self = sum(gene.weight for gene in self.genes.values()) / len(self.genes)
        avg_weight_comp = sum(gene.weight for gene in comparison_genome.genes.values()) / len(comparison_genome.genes)
        return abs(avg_weight_self - avg_weight_comp)


    def mutate(self):
        # Genome Weight Mutations
        for gene in self.genes.values():
            gene.mutate_weight()
        
        # Genome Structural Mutations
        # Adding Gene
        if np.random.uniform() < config.ADD_GENE_MUTATION:

            gene_added = False
            while not gene_added:

                # No valid genes exist to be added.
                if (len(self.hidden_neurons) == 0):
                    break

                # Certain genes are not valid, such as any gene going to an input node, or any gene from an output node
                selected_input_node = np.random.choice(list(set().union(self.hidden_neurons, self.input_neurons)))
                selected_output_node = np.random.choice(list(set().union(self.hidden_neurons, self.output_neurons)))

                gene_valid = True
                for gene in self.genes.values():
                    # If this connection already exists, do not make the new gene
                    if (gene.input_neuron.id == selected_input_node.id and
                        gene.output_neuron.id == selected_output_node.id):
                        gene_valid = False
                        break

                # Can't have loops. Can't connect to itself. Gene must connect node from backwards to forwards.
                if (selected_input_node.id >= selected_output_node.id):
                    gene_valid = False

                if gene_valid:
                    new_gene = Gene(self.innovation.get_new_innovation_number(),
                                    selected_input_node,
                                    selected_output_node)

                    self.genes[new_gene.innovation_number] = new_gene
                    gene_added = True

        # Adding Neuron
        if np.random.uniform() < config.ADD_NODE_MUTATION:

            # Select gene at random and disable
            selected_gene = np.random.choice(self.genes.values())
            
            # Avoid adding the same neuron connection by not choosing a di.
            if selected_gene.enabled:
                selected_gene.disable()

                # Create new node, rearrange ids to make higher neuron ids farther towards output layer
                new_neuron = Neuron(selected_gene.output_neuron.id)
                self.neurons[selected_gene.output_neuron.id] = new_neuron
                selected_gene.output_neuron.set_id(self.get_next_neuron_id())
                self.neurons[selected_gene.output_neuron.id] = selected_gene.output_neuron

                # Create new genes
                new_input_gene = Gene(self.innovation.get_new_innovation_number(),
                                      selected_gene.input_neuron,
                                      new_neuron,
                                      1)

                new_output_gene = Gene(self.innovation.get_new_innovation_number(),
                                       new_neuron,
                                       selected_gene.output_neuron,
                                       selected_gene.weight)

                # Add to network
                self.genes[new_input_gene.innovation_number] = new_input_gene
                self.genes[new_output_gene.innovation_number] = new_output_gene
                self.hidden_neurons.append(new_neuron)

