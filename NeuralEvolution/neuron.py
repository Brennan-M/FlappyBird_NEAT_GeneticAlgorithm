import NeuralEvolution.config as config
import numpy as np
import math



class Neuron(object):


    def __init__(self, neuron_id, n_type="Hidden"):
        self.id = neuron_id
        self.type = n_type

        # Innovation Number : Gene
        self.input_genes = {}
        self.output_genes = {}

        self.expected_inputs = lambda: 1 if self.type == "Input" else len(self.input_genes)
        self.received_inputs = 0
        self.input = 0.0
        self.sent_output = False


    def ready(self):
        received_all_inputs = (self.received_inputs == self.expected_inputs())
        if not self.sent_output and received_all_inputs:
            self.sent_output = True
            return True
        return False


    def reset(self):
        self.received_inputs = 0
        self.input = 0.0
        self.sent_output = False


    def add_input(self, value):
        self.input += value
        self.received_inputs += 1


    def add_input_gene(self, gene):
        self.input_genes[gene.innovation_number] = gene


    def add_output_gene(self, gene):
        self.output_genes[gene.innovation_number] = gene


    def activation(self):
        return self.sigmoid(self.input)


    def sigmoid(self, x):
        #return (1.0 / (1.0 + math.e**(-T)))
        return (2.0 / (1.0 + np.exp(-4.9 * x)) - 1.0)


