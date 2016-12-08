import numpy as np
from scipy.stats import expon
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
        self.species_genome_representative = genome

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
            # I don't particularly like this +1 fix... as it will skew populations
            avg_species_fitness = float(species_fitness)/float(self.species_population+1)
            self.culling(avg_species_fitness)
            return avg_species_fitness if self.active else None
        else:
            return None


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

            fitness_score = ((crash_info['score'] * 1000)       
                              + (crash_info['distance'])        
                              - (distance_from_pipes * 3)       
                              - (1.5 * crash_info['energy']))

            # Should experiment with this more.
            # fitness_score = ((crash_info['distance'])
            #                  - (1.5 * crash_info['energy']))

            neural_networks[crash_info['network_id']].set_fitness(fitness_score)
            species_score += fitness_score

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
            index_choice = self.get_skewed_random_sample(len(replicate_ids))
            random_genome = self.genomes[replicate_ids[index_choice]].clone()

            # Clone
            if np.random.uniform() > config.CROSSOVER_CHANCE:
                genomes[genome_id] = random_genome

            # Crossover
            else:
                index_choice_mate = self.get_skewed_random_sample(len(replicate_ids))
                random_genome_mate = self.genomes[replicate_ids[index_choice_mate]].clone()                
                genomes[genome_id] = self.crossover(random_genome, random_genome_mate)

            # Mutate the newly added genome
            genomes[genome_id].mutate()

            genome_id += 1

        self.genomes = genomes
        

    def crossover(self, random_genome, random_genome_mate):
        if random_genome.fitness > random_genome_mate.fitness:
            fit_genome, unfit_genome = random_genome, random_genome_mate
        else:
            fit_genome, unfit_genome = random_genome_mate, random_genome

        for g_id, gene in fit_genome.genes.items():

            # If it has key, it is a matching gene
            if unfit_genome.genes.has_key(g_id):

                # Randomly inherit from unfit genome
                if np.random.uniform(-1, 1) < 0:
                    gene.weight = unfit_genome.genes[g_id].weight

                # Have chance of disabling if either parent is disabled
                if not gene.enabled or not unfit_genome.genes[g_id].enabled:
                    if np.random.uniform() < config.INHERIT_DISABLED_GENE_RATE:
                        gene.disable()

        return fit_genome


    def select_survivors(self):
        sorted_network_ids = sorted(self.genomes, 
                                    key=lambda k: self.genomes[k].fitness,
                                    reverse=True)

        alive_network_ids = sorted_network_ids[:int(round(float(self.species_population)/2.0))]
        dead_network_ids = sorted_network_ids[int(round(float(self.species_population)/2.0)):]

        return alive_network_ids


    def culling(self, new_avg_fitness):
        if new_avg_fitness > self.avg_max_fitness_achieved:
            self.avg_max_fitness_achieved = new_avg_fitness
            self.generation_with_max_fitness = self.generation_number
        
        # Cull/Repopulate due to stagnation 
        if (self.generation_number - self.generation_with_max_fitness) > self.no_improvement_generations_allowed:
            self.times_stagnated += 1
            if self.times_stagnated > config.STAGNATIONS_ALLOWED:
                print "Species", self.species_id, "culled due to multiple stagnations."
                self.active = False
            else:
                print "Species", self.species_id, "stagnated. Repopulating..."
                self.generation_with_max_fitness = self.generation_number
                self.avg_max_fitness_achieved = 0
                # Get a random genome (just to maintain the structure)
                genome = self.genomes[0]
                self.genomes = {i:genome.clone() for i in xrange(self.species_population)}
                # Reinitialize, otherwise if we just clone the champion, we may end up with same local optima
                for genome in self.genomes.values():
                    genome.reinitialize()

        # Cull due to weak species
        if (self.species_population < config.WEAK_SPECIES_THRESHOLD):
            print "Species", self.species_id, "culled due to lack of breeding resulting in low population."
            self.active = False


    def add_genome(self, genome):
        genome.set_species(self.species_id)
        genome.set_generation(self.generation_number)
        self.genomes[self.species_population] = genome.clone()
        self.species_population += 1


    def delete_genome(self, genome_id):
        self.genomes[genome_id] = self.genomes[self.species_population-1].clone()
        del self.genomes[self.species_population-1]
        self.species_population -= 1


    def set_population(self, population):
        self.species_population = population


    def increment_population(self, population_change=1):
        self.species_population += population_change


    def decrement_population(self, population_change=1):
        self.species_population -= population_change


    def get_skewed_random_sample(self, n, slope=-1.0):
        """
        Randomly choose an index from an array of some given size using a scaled inverse exponential 

        n: length of array
        slope: (float) determines steepness of the probability distribution
               -1.0 by default for slightly uniform probabilities skewed towards the left
               < -1.0 makes it more steep and > -1.0 makes it flatter
               slope = -n generates an approximately uniform distribution
        """
        inv_l = 1.0/(n**float(slope)) # 1/lambda
        x = np.array([i for i in range(0,n)]) # list of indices 

        # generate inverse exponential distribution using the indices and the inverse of lambda
        p = expon.pdf(x, scale=inv_l)

        # generate uniformly distributed random number and weigh it by total sum of pdf from above
        rand = np.random.random() * np.sum(p)
        
        for i, p_i in enumerate(p):
            # chooses an index by checking whether the generated number falls into a region around 
            # that index's probability, where the region is sized based on that index's probability 
            rand -= p_i
            if rand < 0:
                return i

        return 0


    def pretty_print_s_id(self, s_id):
        print "\n"
        print "===================="
        print "===  Species:", s_id, " ==="
        print "===================="
        print "\n"


    def pretty_print_gen_id(self, gen_id):
        print "-----------------------"
        print "---  Generation:", gen_id, " ---"
        print "-----------------------"
        print "\n"

