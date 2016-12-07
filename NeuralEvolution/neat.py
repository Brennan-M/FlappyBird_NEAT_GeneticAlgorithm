from NeuralEvolution.species import Species
from NeuralEvolution.network import Network
from NeuralEvolution.innovation import Innovation
import NeuralEvolution.config as config
import math



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
        self.create_new_species(initial_genome, self.population)


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
            for genome_index, genome in s.genomes.items():
                if not genome.is_compatible(s.species_genome_representative):
                    s.delete_genome(genome_index)
                    self.assign_genome(genome, s_id)


    def assign_genome(self, genome, origin_species_id):
        print "Assigning", genome
        for s_id, s in self.species.items():
            if genome.is_compatible(s.species_genome_representative):
                s.add_genome(genome)
                return

        population = int(math.ceil(self.species[origin_species_id].species_population/2.0))
        # Halving the population for the origin species, will take one generation for changes to propagate
        self.species[origin_species_id].set_population(population)
        self.create_new_species(genome, population)


    def create_new_species(self, initial_species_genome, population):
        self.species[self.num_species] = Species(self.num_species, population, initial_species_genome)
        self.num_species += 1

