import numpy as np
from NeuralEvolution.network import Network
import FlapPyBird.flappy as flpy
import os
os.chdir(os.getcwd() + '/FlapPyBird/')



class Species(object):


    def __init__(self, topology, num_generations, num_networks_per_gen, s_id):

        self.species_id = s_id
        self.num_generations = num_generations
        self.num_networks_per_gen = num_networks_per_gen
        self.organism_topology = topology
        self.generations = {}
        self.max_fitness_score = None


    def evolve(self):
        replicated_network_ids = None
        for gen in xrange(self.num_generations):
            self.create_generation(gen, replicated_network_ids)
            self.generate_fitness(gen)
            replicated_network_ids = self.select_survivors(gen)


    def create_generation(self, generation_number, replicate_ids):
        networks = {}

        # Create a non-inherited generation
        if (not replicate_ids):
            for network_number in xrange(self.num_networks_per_gen):
                network_info = {"network": network_number, 
                                "generation": generation_number,
                                "species": self.species_id}

                new_neural_network = Network(self.organism_topology, network_info)
                networks[network_number] = new_neural_network

        # Spawn a generation consisting of progeny from fittest predecessors
        elif (replicate_ids): 
            network_number = 0
            for r_id in replicate_ids:

                parent_network = self.generations[generation_number-1][r_id]

                for i in range(2):

                    # Mutated progenies
                    network_info_mutation = {"network": network_number, 
                                             "generation": generation_number,
                                             "species": self.species_id}

                    mutated_neural_network = Network(self.organism_topology,
                                                     network_info_mutation,
                                                     parent_network.get_genes())
                    mutated_neural_network.mutate()
                    networks[network_number] = mutated_neural_network

                    network_number += 1


        self.generations[generation_number] = networks


    # This function holds the interface and interaction with FlapPyBird
    def generate_fitness(self, generation_number):
        generation_score = 0
        
        self.pretty_print_gen_id(generation_number)

        neural_networks = self.generations[generation_number].values()
        # Run the game with each network in the current generation
        app = flpy.FlappyBirdApp(neural_networks)
        app.play()
        birds = app.birds

        for network_num, bird in enumerate(birds):
            print bird
            crashInfo = bird.crashInfo
            distance_from_pipes = 0
            if (bird.y < crashInfo['upperPipes'][0]['y']):
                distance_from_pipes = abs(bird.y - crashInfo['upperPipes'][0]['y'])
            elif (bird.y > crashInfo['upperPipes'][0]['y']):
                distance_from_pipes = abs(bird.y - crashInfo['lowerPipes'][0]['y'])

            # A couple different fitness functions to mess with
            # fitness_score = (crashInfo['score']*1000) + \
            #                crashInfo['distance'] - \
            #                distance_from_pipes - \
            #                (crashInfo['energy'] * 2)

            fitness_score = ((crashInfo['score'] * 5000) 
                              + (crashInfo['distance'])
                              - (distance_from_pipes * 3))

            neural_networks[network_num].set_fitness(fitness_score)


            print 'Network', network_num, 'scored', fitness_score
            generation_score += fitness_score

        print "\nGeneration Score:", generation_score
        

    def select_survivors(self, generation_number):
        sorted_network_ids = sorted(self.generations[generation_number], 
                                    key=lambda k: self.generations[generation_number][k].fitness,
                                    reverse=True)

        alive_network_ids = sorted_network_ids[:self.num_networks_per_gen/2]
        dead_network_ids = sorted_network_ids[self.num_networks_per_gen/2:]

        print '\nBest Networks:', alive_network_ids
        return alive_network_ids


    def pretty_print_gen_id(self, gen_id):
        print "\n"
        print "-----------------------"
        print "---  Generation:", gen_id, " ---"
        print "-----------------------"
        print "\n"


