from NeuralEvolution.neat import NEAT
import sys



# Driver for NEAT solution to FlapPyBird
def evolutionary_driver():
	solver = NEAT()
	solution_genome = solver.start_evolutionary_process()
	write_genome_to_file(solution_genome)


def write_genome_to_file(genome):
    # Write the genome that solves it to a file
    pass


if __name__ == "__main__":
	evolutionary_driver()
