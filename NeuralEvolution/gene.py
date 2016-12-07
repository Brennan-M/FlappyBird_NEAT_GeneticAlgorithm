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
        self.weight = weight

        if self.weight is None:
            self.randomize_weight()


    def mutate_weight(self):
        # Weight Mutation
        if np.random.uniform() < config.WEIGHT_MUTATION_RATE:
            if np.random.uniform() < config.UNIFORM_WEIGHT_MUTATION_RATE:
                self.weight += np.random.uniform(-0.1, 0.1)
            else:
                self.randomize_weight()

        # Enabled Mutation
        if not self.enabled:
            if np.random.uniform() < config.ENABLE_GENE_MUTATION_RATE:
                self.enabled = True


    def randomize_weight(self):
        self.weight = np.random.uniform(-2, 2)


    def disable(self):
        self.enabled = False


    def copy(self):
        return Gene(innovation_number=self.innovation_number,
                    input_neuron_id=self.input_neuron_id,
                    output_neuron_id=self.output_neuron_id,
                    weight=self.weight,
                    enabled=self.enabled)

