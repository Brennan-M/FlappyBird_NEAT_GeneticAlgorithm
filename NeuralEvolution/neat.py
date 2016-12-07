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

            avg_fitness_scores = [None for i in xrange(self.num_species)]
            # Run the current generation for each species
            for s_id, s in self.species.items():
                avg_fitness = s.run_generation()
                avg_fitness_scores[s_id] = avg_fitness
            
            self.avg_population_fitness = float(sum(avg_fitness_scores))

            if (self.avg_population_fitness == 0):
                print "\n\nAll species have gone extinct!\n\n"
                exit()

            # Evolve (create the next generation) for each species
            for s_id, s in self.species.items():
                weighted_fitness = avg_fitness_scores[s_id]/self.avg_population_fitness
                weighted_population = int(round(self.population * weighted_fitness))
                s.set_population(weighted_population)
                s.evolve()

            self.perform_speciation()

        # Need to potentially set this somewhere...
        return self.solution_genome

    
    def perform_speciation(self):
        for s_id, s in self.species.items():
            for genome in s.genomes:
                pass
            # If it doesnt belong in current species, check if it belongs in any other current species
            # otherwise, create new species, with this new species created, need to adjust population
            #   of species it came from and new species


    def is_unique_genome(self, genome):
        # My Code Here
        pass


    def create_new_species(self, initial_species_genome):
        self.species[self.num_species] = Species(self.num_species, self.population, initial_species_genome)
        self.num_species += 1

