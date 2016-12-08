from NeuralEvolution.species import Species
from NeuralEvolution.network import Network
from NeuralEvolution.innovation import Innovation
import NeuralEvolution.config as config
from sklearn import preprocessing
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

            avg_fitness_scores = {}
            # Run the current generation for each species
            for s_id, s in self.species.items():
                avg_fitness = s.run_generation()
                if avg_fitness != None:
                    avg_fitness_scores[s_id] = avg_fitness
            
            if (len(avg_fitness_scores) == 0):
                print "\n\nAll species have gone extinct!\n\n"
                exit()

            if config.DYNAMIC_POPULATION:
                self.assign_species_populations_for_next_generation(avg_fitness_scores)

            # Evolve (create the next generation) for each species
            for s_id, s in self.species.items():
                s.evolve()

            # Create new species from evolved current species
            if config.SPECIATION:
                self.perform_speciation()

        # Need to potentially set this somewhere...
        return self.solution_genome


    def assign_species_populations_for_next_generation(self, avg_fitness_scores):
        if len(avg_fitness_scores) == 1:
            return

        sorted_species_ids = sorted(avg_fitness_scores, key=avg_fitness_scores.get)

        # If any species were culled... reassign population to best species.
        active_pop = self.get_active_population()
        if active_pop < self.population:
            print "Active population:", active_pop
            print sorted_species_ids
            self.species[sorted_species_ids[0]].increment_population(self.population-active_pop)

        # Handle all other population changes.
        pop_change = int(math.floor(len(avg_fitness_scores)/2.0))
        start = 0
        end = len(sorted_species_ids) - 1
        while (start < end): 
            self.species[sorted_species_ids[start]].decrement_population(pop_change)
            self.species[sorted_species_ids[end]].increment_population(pop_change)
            start += 1
            end -= 1
            pop_change -= 1

    
    def perform_speciation(self):
        for s_id, s in self.species.items():
            # Only want to speciate and find evolve from active species
            if s.active:
                for genome_index, genome in s.genomes.items():
                    if not genome.is_compatible(s.species_genome_representative):
                        self.assign_genome(genome, s_id)
                        s.delete_genome(genome_index)


    def assign_genome(self, genome, origin_species_id):
        for s_id, s in self.species.items():
            if genome.is_compatible(s.species_genome_representative):
                # If we add to dead species, it didn't deserve to live anyway
                s.add_genome(genome)
                return

        # Not my favorite way of deciding on new populations...
        if config.DYNAMIC_POPULATION:
            new_species_pop = int(math.floor(self.species[origin_species_id].species_population/2.0))
            origin_species_pop = int(math.ceil(self.species[origin_species_id].species_population/2.0))
            self.species[origin_species_id].set_population(origin_species_pop)
        else:
            new_species_pop = self.population

        self.create_new_species(genome, new_species_pop)


    def create_new_species(self, initial_species_genome, population):
        self.species[self.num_species] = Species(self.num_species, population, initial_species_genome)
        self.num_species += 1


    def get_active_population(self):
        active_population = 0
        for species in self.species.values():
            if species.active:
                active_population += species.species_population

        return active_population

