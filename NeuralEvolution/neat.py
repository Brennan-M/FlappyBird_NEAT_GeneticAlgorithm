from NeuralEvolution.species import Species
from NeuralEvolution.network import Network
from NeuralEvolution.innovation import Innovation
import NeuralEvolution.config as config



class NEAT(object):


    def __init__(self):

        self.solved = False
        self.solution_genome = None

        self.population = config.POPULATION
        self.initial_genome_topology = (config.INPUT_NEURONS, config.OUTPUT_NEURONS)

        self.num_species = 0
        self.species = {}

        self.population_fitness = 0

        self.innovation = Innovation()

        initial_genome = Network(self.initial_genome_topology, self.innovation)
        self.create_new_species(initial_genome)


    def start_evolutionary_process(self):

        while not self.solved:

            fitness_scores = [None for i in xrange(self.num_species)]
            # Run the current generation for each species
            for s_id, s in self.species.items():
                fitness = s.run_generation()
                fitness_scores[s_id] = fitness
            
            self.population_fitness = float(sum(fitness_scores))

            # Evolve (create the next generation) for each species
            for s_id, s in self.species.items():
                weighted_fitness = fitness_scores[s_id]/self.population_fitness
                weighted_population = int(round(self.population * weighted_fitness))
                s.set_population(weighted_population)
                s.evolve()

        # Need to potentially set this somewhere...
        return self.solution_genome

    
    def create_new_species(self, initial_species_genome):
        self.species[self.num_species] = Species(self.num_species, self.population, initial_species_genome)
        self.num_species += 1


    def is_unique_genome(self, genome):
        # My Code Here
        pass

