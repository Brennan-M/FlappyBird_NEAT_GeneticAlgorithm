import numpy as np
from NeuralEvolution.network import Network
import NeuralEvolution.config as config
import FlapPyBird.flappy as flpy
import os
os.chdir(os.getcwd() + '/FlapPyBird/')



class Species(object):


    def __init__(self, s_id, species_population, genome):
        self.species_id = s_id
        self.species_population = species_population
        self.generation_number = 0

        genome.set_species(self.species_id)
        genome.set_generation(self.generation_number)
        self.genomes = {i:genome.clone() for i in xrange(self.species_population)}
        for i in xrange(1, self.species_population):
            self.genomes[i].reinitialize()

        # Information used for culling and population control
        self.active = True
        self.no_improvement_generations_allowed = config.STAGNATED_SPECIES_THRESHOLD
        self.times_stagnated = 0
        self.avg_max_fitness_achieved = 0
        self.generation_with_max_fitness = 0


    def run_generation(self):
        if self.active:
            species_fitness = self.generate_fitness()
            self.culling(species_fitness)
            return species_fitness if self.active else 0
        else:
            return 0


    def evolve(self):
        if self.active:
            survivor_ids = self.select_survivors()
            self.create_next_generation(survivor_ids)
            self.generation_number += 1
            for genome in self.genomes.values():
                genome.set_generation(self.generation_number)


    # This function holds the interface and interaction with FlapPyBird
    def generate_fitness(self):
        species_score = 0
        
        self.pretty_print_s_id(self.species_id)
        self.pretty_print_gen_id(self.generation_number)

        neural_networks = self.genomes.values()

        # Run the game with each organism in the current generation
        app = flpy.FlappyBirdApp(neural_networks)
        app.play()
        results = app.crash_info

        for crash_info in results:

            distance_from_pipes = 0
            if (crash_info['y'] < crash_info['upperPipes'][0]['y']):
                distance_from_pipes = abs(crash_info['y'] - crash_info['upperPipes'][0]['y'])
            elif (crash_info['y'] > crash_info['upperPipes'][0]['y']):
                distance_from_pipes = abs(crash_info['y'] - crash_info['lowerPipes'][0]['y'])

            # fitness_score = ((crash_info['score'] * 5000) 
            #                   + (crash_info['distance'])
            #                   - (distance_from_pipes * 3))

            fitness_score = ((crash_info['distance'])
                              - (1.5 * crash_info['energy']))

            neural_networks[crash_info['network_id']].set_fitness(fitness_score)

            species_score += fitness_score

        for n_id, net in self.genomes.items():
            print 'Network', n_id, 'scored', net.fitness

        print "\nSpecies Score:", species_score

        return species_score


    def create_next_generation(self, replicate_ids):
        genomes = {}

        # Champion of each species is copied to next generation unchanged
        genomes[0] = self.genomes[replicate_ids[0]].clone()
        genome_id = 1

        # Spawn a generation consisting of progeny from fittest predecessors
        while (genome_id < self.species_population):

            # Choose an old genome at random from the survivors
            choice = np.random.choice(replicate_ids)
            random_genome = self.genomes[choice].clone()

            # Clone
            if np.random.uniform() > config.CROSSOVER_CHANCE:
                genomes[genome_id] = random_genome

            # Crossover
            else:
                # genome_mate = self.genomes[np.random.choice(replicate_ids)]
                # genomes[genome_id] = random_genome.crossover(genome_mate)
                genomes[genome_id] = random_genome

            # Mutate the newly added genome
            genomes[genome_id].mutate()

            genome_id += 1

        self.genomes = genomes
        

    def select_survivors(self):
        sorted_network_ids = sorted(self.genomes, 
                                    key=lambda k: self.genomes[k].fitness,
                                    reverse=True)

        alive_network_ids = sorted_network_ids[:int(round(float(self.species_population)/2.0))]
        dead_network_ids = sorted_network_ids[int(round(float(self.species_population)/2.0)):]

        print '\nBest Networks:', alive_network_ids
        print 'Worst Networks:', dead_network_ids
        return alive_network_ids


    def culling(self, new_fitness):
        new_avg_fitness = (new_fitness / self.species_population)
        if new_avg_fitness > self.avg_max_fitness_achieved:
            self.avg_max_fitness_achieved = new_avg_fitness
            self.generation_with_max_fitness = self.generation_number
        
        # Cull due to stagnation 
        if (self.generation_number - self.generation_with_max_fitness) > self.no_improvement_generations_allowed:
            self.times_stagnated += 1
            # Could do a type of repopulation here, and allow for 3 stagnations
            print "Species", self.species_id, "culled."
            self.active = False

        # Cull due to weak species
        if (self.species_population < config.WEAK_SPECIES_THRESHOLD):
            print "Species", self.species_id, "culled."
            self.active = False


    def set_population(self, population):
        self.species_population = population


    def pretty_print_s_id(self, s_id):
        print "\n"
        print "===================="
        print "===  Species:", s_id, " ==="
        print "===================="
        print "\n"


    def pretty_print_gen_id(self, gen_id):
        print "\n"
        print "-----------------------"
        print "---  Generation:", gen_id, " ---"
        print "-----------------------"
        print "\n"

