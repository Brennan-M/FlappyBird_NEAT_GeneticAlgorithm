from NeuralEvolution.neat import NEAT


PERCEPTRON = 0
NET = 1
DEEP_NET = 2

# Driver for NEAT solution to FlapPyBird
def evolutionary_driver(network_options):
	# Pass in:
	#	 Topology of an organism (type, input neurons, output neurons, hidden neurons, hidden layers)
	#	 Number of species to create
	#	 Number of generations per species
	#	 Number of organisms/networks per generation
	solver = NEAT(network_options, 5, 10000, 10)
	solver.start_evolutionary_process()


if __name__ == "__main__":

	net_type = NET
	input_neurons = 10
	output_neurons = 1
	# Irrelevant if net_type is PERCEPTRON
	hidden_neurons = 5
	hidden_layers = 1

	params = (net_type, input_neurons, output_neurons, hidden_neurons, hidden_layers)

	evolutionary_driver(params)
