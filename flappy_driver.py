from NeuralEvolution.neat import NEAT
import sys



# Driver for NEAT solution to FlapPyBird
def evolutionary_driver(network_options):
	# Pass in:
	#	 Topology of an organism (input neurons, output neurons, hidden neurons, hidden layers)
	#	 Number of species to create
	#	 Number of generations per species
	#	 Number of organisms/networks per generation
	solver = NEAT(network_options, 5, 10000, 10)
	solver.start_evolutionary_process()


if __name__ == "__main__":

	def_input_neurons = 10
	def_output_neurons = 1
	def_hidden_neurons = 2
	def_hidden_layers = 1

	options = {}
	options['-i'] = def_input_neurons
	options['-o'] = def_output_neurons
	options['-h'] = def_hidden_neurons
	options['-l'] = def_hidden_layers

	if (len(sys.argv) > 1):
		for i in range(1, len(sys.argv), 2):
			options[sys.argv[i]] = int(sys.argv[i+1])

	params = (options['-i'], options['-o'], options['-h'], options['-l'])

	evolutionary_driver(params)
