import NeuralEvolution.config as config
import numpy as np



class Gene(object):


    def __init__(self, innovation_number, input_neuron, output_neuron, weight=None, enabled=True):

        self.innovation_number = innovation_number

        self.input_neuron = input_neuron
        input_neuron.add_output_gene(self)

        self.output_neuron = output_neuron
        output_neuron.add_input_gene(self)

        self.enabled = enabled

        if weight is None:
            weight = np.random.uniform(-1, 1)

        self.weight = weight


    def randomize_weight(self):
        self.weight = np.random.uniform(-1, 1)


    def copy(self):
        return Gene(innovation_number=self.innovation_number,
                    input_neuron_id=self.input_neuron_id,
                    output_neuron_id=self.output_neuron_id,
                    weight=self.weight,
                    enabled=self.enabled)

