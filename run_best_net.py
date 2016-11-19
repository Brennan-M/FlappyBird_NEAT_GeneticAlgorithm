import numpy as np
from NeuralEvolution.network import Network
import FlapPyBird.flappy as flpy
import os
os.chdir(os.getcwd() + '/FlapPyBird/')



PERCEPTRON = 0
NET = 1
DEEP_NET = 2


# This is just meant as a simple script, and is largely duplicated code.
def run_net_from_file(filename):

	try:
		f = open(filename, 'r')

		fitness = float(f.readline())
		structure = int(f.readline())
		ids = [int(n) for n in f.readline().rstrip().split(" ")]
		network_info = {"network": ids[2], 
		                "generation": ids[1],
		                "species": ids[0]}
		topology = [int(t) for t in f.readline().rstrip().split(" ")]

		neural_network = None

		if structure == PERCEPTRON:
			weights = [float(w) for w in f.readline().rstrip().split(" ")]
			bias = [float(f.readline().rstrip())]

			neural_network = Network(topology,
			                         network_info,
			                         (weights, bias))

		elif structure == NET:
			hidden_neurons = topology[2]

			weights = [float(w) for w in f.readline().rstrip().split(" ")]
			input_w = [weights[i:i+hidden_neurons] for i in range(0, len(weights), hidden_neurons)]
			output_w = [[float(w)] for w in f.readline().rstrip().split(" ")]
			bias = [[float(b)] for b in f.readline().rstrip().split(" ")]

			neural_network = Network(topology,
			                         network_info,
			                         (input_w, output_w, bias))


		elif structure == DEEP_NET:
			pass

		# Run the neural net retreived from the file above
		fitness_score = 0
		while (fitness_score < fitness):
			results = flpy.main(neural_network)

			distance_from_pipes = 0
			if (results['y'] < results['upperPipes'][0]['y']):
			    distance_from_pipes = abs(results['y'] - results['upperPipes'][0]['y'])
			elif (results['y'] > results['upperPipes'][0]['y']):
			    distance_from_pipes = abs(results['y'] - results['lowerPipes'][0]['y'])

			fitness_score = (results['score']*1000) + \
			                results['distance'] - \
			                distance_from_pipes - \
			                (results['energy'] * 2)

	except:
		print "File Not Found... Or Error Encountered."



if __name__ == "__main__":
	run_net_from_file("../BestNetworks/(10, 1, 2, 1).best_network.flpynet")

