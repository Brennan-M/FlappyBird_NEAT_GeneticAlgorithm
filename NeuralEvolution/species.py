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
        self.max_fitness_score = self.read_fitness_from_file()

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

        for network_num, network in self.generations[generation_number].items():
            # Run the game with each network in the current generation
            results = flpy.main(network)

            distance_from_pipes = 0
            if (results['y'] < results['upperPipes'][0]['y']):
                distance_from_pipes = abs(results['y'] - results['upperPipes'][0]['y'])
            elif (results['y'] > results['upperPipes'][0]['y']):
                distance_from_pipes = abs(results['y'] - results['lowerPipes'][0]['y'])

            # A couple different fitness functions to mess with
            fitness_score = (results['score']*1000) + \
                            results['distance'] - \
                            distance_from_pipes - \
                            (results['energy'] * 2)

            # fitness_score = ((results['score'] * 5000) 
            #                  + (results['distance'])
            #                  - (distance_from_pipes * 3))

            network.set_fitness(fitness_score)

            if fitness_score > self.max_fitness_score:
                self.max_fitness_score = fitness_score
                self.write_net_to_file(network)

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


    # Utility functions for saving networks with file I/O #
    # --------------------------------------------------- #


    def generate_filename(self):
        return "../BestNetworks/" + str(self.organism_topology) + ".best_network.flpynet"


    def read_fitness_from_file(self):
        try:
            f = open(self.generate_filename(), 'r')
            fitness_score = f.readline()
            return float(fitness_score)
        except:
            return float("-inf")


    def write_net_to_file(self, network):
        f = open(self.generate_filename(), 'w')

        f.write(str(network.fitness) + "\n")
        f.write(str(network.structure_type) + "\n")

        f.write(str(network.species_number) + 
                " " + str(network.generation_number) +
                " " + str(network.network_number) + 
                "\n")

        for t in self.organism_topology:
            f.write(str(t) + " ")
        f.write("\n")

        if network.structure_type == 0:
            weights, bias = network.get_genes()

            for w in weights:
                f.write(str(w) + " ")
            f.write("\n")
            f.write(str(bias[0][0]) + "\n")

        elif network.structure_type == 1:
            input_w, output_w, bias = network.get_genes()

            for seq in input_w:
                for w in seq:
                    f.write(str(w) + " ")
            f.write("\n")
            for seq in output_w:
                for w in seq:
                    f.write(str(w) + " ")
            f.write("\n")
            for b in bias:
                f.write(str(b[0]) + " ")
            f.write("\n")

        elif network.structure_type == 2:
            pass

