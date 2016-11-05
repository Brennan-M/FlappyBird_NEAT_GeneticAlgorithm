import numpy as np
import modules.flappy as flpy
from modules.ann_interface_custom import *


class Species:

    def __init__(self, networks_per_generation=10, species_ID=0):

        self.species_ID = species_ID


        # Set number of networks in each generation
        self.networks_per_generation = networks_per_generation

        # Set current generation number; parent = 0
        self.current_generation_number = 0

        # Initialize empty generations list to track all generations through evolution
        self.generations = []

        # Initialize parent generation with initial networks
        self._init_parent_()

        # Initialize list to contain top networks of each generation
        self.top_networks = []

        

          

    def _init_parent_(self):
        """
            Initialize the parent generation with X number of networks
                where X = self.networks_per_generation

                Each network is initialized with its position in the generation,
                in addition to its generation number.
        """
        parent_gen = []
        for network_ID in range(self.networks_per_generation):
            generation_ID = 0
            parent_gen.append(Interface(network_ID, generation_ID, speciesID=self.species_ID))

        self.generations.append(parent_gen)
        


    def generate_fitness(self):
        """
            Generates the fitness for each network in the generation.
            The fitness is a measured by each networks performance 
                (i.e. the score it achieves playing Flappy Birds)
        """
        current_generation = self.generations[self.current_generation_number]
        
        print("\n*$-------------========================-------------$*")
        print("\t\t   Generation {}".format(self.current_generation_number))
        print("*$-------------========================-------------$*")

        for network in current_generation:
            print("\n\tNetwork {}".format(network.network_ID))
            print("\t----------")
            print("\tTopology: {}".format(network.network.topology))

            results = flpy.main(network)
            fitness_score = results['score']

            # Check if not scored even 1 point
            if fitness_score == 0:
                
                # Check if bird flaps only once then eats it. This is fitness = 0!
                if results['groundCrash']:
                    fitness_score = 0

                # Check if bird flies above map. This is never good, so fitness = 0!
                elif results['y'] <= 0:
                    fitness_score = 0
                
                # Bird is doing something reasonable. Now we want to select for minimal energy expenditure and max distance
                else:
                    fitness_score = max(results['distance'] - 2*results['energy'], 0)

            # At least 1 point has been scored.
            elif fitness_score >= 1:
                fitness_score = fitness_score * 10000 - results['energy']

            network.set_fitness(fitness_score)
            print("\tDistance: {}".format(results['distance']))
            print("\ty: {}".format(results['y']))
            print("\tFitness: {}".format(fitness_score))

        
        


    def selection(self):
        """
            Selection iterates over the current generation's network fitnesses   
            The top network is selected and produces X new progeny
            Each child has a chance for mutation: call replication()
                1. Change in neural network weights
                2. Change in hidden layer neuron number (addition or substraction of a node)
            The result is a new generation with X new progeny posed for a new round of selection
        """

        print("\n")
        print("\t=====================")
        print("\t      Selection      ")
        print("\t=====================")
        generations = self.generations[self.current_generation_number]

        max_fitness = generations[0].fitness
        top_network = generations[0]

        """ Just pretend that bubble sort isn't being used. """
        top_networks = []
        sorted_ = False
        i = 0
        while not sorted_:
            sorted_ = True

            for index, network in enumerate(generations[:-1]):
                if network.fitness < generations[index+1].fitness:
                    temp = network
                    generations[index] = generations[index+1]
                    generations[index+1] = temp
    
                    sorted_ = False
        
        self.top_networks = generations[:int(len(generations)/2)]

        

        print("\n\tTop Networks")
        for top_net in self.top_networks:
            print("\tNetwork {}".format(top_net.network_ID))
            print("\tFitness: {}\n".format(top_net.fitness))
        



    def replication(self):
        """

        """
        print("\n")
        print("\t=====================")
        print("\t     Replication     ")
        print("\t=====================")

        progeny = []
        new_net_ID = 0
        for top_network in self.top_networks:
            print("\n\tReplicating network {}...".format(top_network.network_ID))    
            print("\t-----------------")
            print("\tFitness: {}".format(top_network.fitness))
            mutations = top_network.mutate()
            new_network = Interface(new_net_ID, self.current_generation_number+1, self.species_ID, mutations)
            new_net_ID += 1

            top_network_copy = Interface(new_net_ID, self.current_generation_number+1, self.species_ID, copy=top_network)
            new_net_ID += 1

            progeny.append(new_network)
            progeny.append(top_network_copy)


        self.generations.append(progeny)

        self.current_generation_number += 1


    def check_extinct(self):

        all_zero_fitness = True
        for network in self.generations[self.current_generation_number]:

            if network.fitness != 0:
                all_zero_fitness = False

        if all_zero_fitness:
            return True
        else:
            return False




    def expand_population(self, organisms):
        print("\n\n\tExpanding population...\n")

    
        for network in self.generations[self.current_generation_number]:
            if network.fitness > 0:
                successful_network = network

        progeny = [successful_network, successful_network]

        for organism_ID in range(organisms-2):
            mutations = successful_network.mutate()
            new_network = Interface(organism_ID, self.current_generation_number+1, self.species_ID, mutations)
            progeny.append(new_network)
            

        self.generations.append(progeny)
        self.current_generation_number += 1




