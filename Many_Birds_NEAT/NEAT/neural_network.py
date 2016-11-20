import numpy as np
from sklearn.preprocessing import normalize
from NEAT.neuron import Neuron


MAX_HIDDEN_NEURONS = 20
connection_weight_mutation_chance = 0.8
chance_of_each_weight_uniform_mutation = 0.9
chance_of_each_weight_randomly_mutated = 0.1
chance_disable_inherited_gene = 0.75
chance_mutation_NO_crossover = 0.25
chance_interspecies_mating = 0.001
chance_new_node = 0.03


class Matrix:

	def __init__(self, outsize, insize):
		self.out_size = outsize
		self.in_size = insize
		self.W = np.zeros((outsize, insize))

	def _set_W_(self):
		pass


class Neural_Network:

	def __init__(self, topology, genes=None):
		self.topology = topology

		if not genes:
			self._set_layer_dimensions_()
			self._set_matrices_()
			self._init_weights_()
		else:
			self.W = genes[0]
			self.b = genes[1]
			self.mutate_genes()


	def mutate_genes(self):
		for layer_index, layer in enumerate(self.W):
			for row_index, row in enumerate(layer):
				for weight_index, weight in enumerate(row):

					# determine whether weight is 0 or none 0
					link_exists = True if weight !=0 else False
					if link_exists:
						link_mutation_chance = np.random.uniform()
						if link_mutation_chance <= connection_weight_mutation_chance:
							uniform_chance = np.random.uniform()
							if uniform_chance <= chance_of_each_weight_uniform_mutation:
								weight += uniform_chance
							else:
								weight += np.random.randn()
					elif not link_exists:
						if layer_index != len(self.topology)-1:
							new_node_chance = np.random.uniform()
							if new_node_chance <= chance_new_node:
								weight = 1
								try:
									self.W[layer_index+1][row_index][weight_index] = np.random.uniform()
								except:
									pass


	def _set_layer_dimensions_(self):
		self.in_size = self.topology[0]
		self.out_size = self.topology[-1]
		self.hidden = False

		if len(self.topology) > 2:
			self.hidden = True


	def _set_matrices_(self):
		self.W = []
		self.b = []

		num_total_layers = len(self.topology)

		for layer in range(num_total_layers):
			# Input Layer
			if layer == 0:
				in_size = self.in_size
				out_size = MAX_HIDDEN_NEURONS

			# Output Layer
			elif layer == num_total_layers-1:
				in_size = MAX_HIDDEN_NEURONS
				out_size = self.out_size

			# Hidden layers
			else:
				in_size = out_size = MAX_HIDDEN_NEURONS

			# Create and append W and b
			self.W.append(np.zeros((out_size, in_size)))
			self.b.append(np.zeros(out_size))


	def _init_weights_(self):

		for index, matrix in enumerate(self.W[:-1]):

			num_neurons_next_layer = self.topology[index+1]

			for row_index, row in enumerate(matrix):
				if row_index < num_neurons_next_layer:
					matrix[row_index] = np.random.randn(len(row))
					self.b[index][row_index] = 1


	def _activation_(self, X, size_output):

		output = np.zeros(len(X))
		for index in range(size_output):
			output[index] = 1 / (1 + np.exp(-4.9*X[index]))

		return output


	def feed_forward(self, X):
		X = np.asarray(X)
		for index, (matrix, b) in enumerate(zip(self.W[:-1], self.b)):

			size_output = self.topology[index+1]

			if index == 0:

				X = normalize(X[:,np.newaxis], axis=0).ravel()
				dot_ = np.dot(matrix, X)

			else:
				dot_ = np.dot(matrix, output)

			output = self._activation_(dot_ + b, size_output)

		self.output = output[0]

	def decision(self):
		return 0 if self.output < 0.5 else 1


	def print_matrices(self):
		print("Matrices")
		for index, layer in enumerate(self.W):
			print("W{}".format(index+1))
			print(layer)
			print("\n")

		for b in self.b:
			print("b: {}".format(b))


	def copy_genes(self):
		W = np.copy(self.W)
		b = np.copy(self.b)

		return self.topology, [W, b]


if __name__ == "__main__":
	topology = [8, 5, 10, 1]
	net = Neural_Network(topology)

	#net.print_matrices()

	input_X = [0, 1, 0, 1, 1, 0, 1, 1]
	net.feed_forward(input_X)

	print("\nTopology: {}".format(topology))
	print("\nInput: {}".format(input_X))
	print("\nOutput: {}\n".format(net.output))
