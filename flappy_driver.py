from NeuralEvolution.neat import NEAT


# Driver for NEAT solution to FlapPyBird
def evolutionary_driver():
	# Pass in:
	#	 Topology of an organism (input-output neurons)
	#	 Number of species to create
	#	 Number of generations per species
	#	 Number of organisms/networks per generation
	solver = NEAT((6,1), 5, 5, 10)
	solver.start_evolutionary_process()


if __name__ == "__main__":
	evolutionary_driver()
