import numpy as np
import modules.flappy as flpy
from modules.ann_interface_custom import *

"""
Species Class
-------------

This class tracks each species and its generations through selection.

This is also where the fitness, selection, and replication functionality is held.

Each species object is initialized with a parent generation with randomly generated networks (neural_network.py)

The sequence from engine.py is, for each network in current generation:

    1. Generate Fitness
        results = flpy.main(network) applies the current network to the game and generates results
        These results are used to generate the network's fitness.

    2. Selection
        The top networks are selected to be reproduced

    3. Replication
        The top networks chosen in step 2 are replicated with mutation and stored as the progeny, the next generation
        The generation number is incremented, and this process repeats

"""

class Species:

    def __init__(self, networks_per_generation=10, species_ID=0):

        self.species_ID = species_ID

        # Set number of networks in each generation
        self.networks_per_generation = networks_per_generation

        # Initialize parent generation with initial networks
        self._init_parent_()

        


    def _init_parent_(self):
        """
            Initialize the parent generation with X number of networks
                where X = self.networks_per_generation

                Each network is initialized with its position in the generation,
                in addition to its generation number.
        """
        # Set current generation number; parent = 0
        self.current_generation_number = 0

        # Initialize empty generations list to track all generations through evolution
        self.generations = []

        parent_gen = []
        for network_ID in range(self.networks_per_generation):
            generation_ID = 0
            ID = {"network": network_ID, "generation": generation_ID, "species": self.species_ID}

            parent_gen.append(Network(ID))

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
            print("\tTopology: {}".format(network.topology))
            try:
                print("\tParent's Fitness: {}".format(network.parent_fitness))
            except:
                pass

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
        # Initialize list to contain top networks of each generation
        self.top_networks = []

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
        print("\t-----------")
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

        new_generation = []
        new_net_ID = 0
        
        ID = { "network": 0, 
               "generation": self.current_generation_number+1, 
               "species": self.species_ID }

        for top_network in self.top_networks:
            
            print("\n\tReplicating network {}...".format(top_network.network_ID))    
            print("\t-----------------")
            print("\tFitness: {}".format(top_network.fitness))
            

            # Progeny 1 Replication -----------------------------------------------------------
            progeny_1 = Network(ID, top_network, mutation=False)
            ID["network"] += 1
            # ---------------------------------------------------------------------------------

            # Progeny 2 Replication -----------------------------------------------------------
            progeny_2 = Network(ID, top_network, mutation=True)
            ID["network"] += 1
            # ---------------------------------------------------------------------------------


            # Append progeny to new generation
            new_generation.append(progeny_1)
            new_generation.append(progeny_2)
            ID["generation"] += 1


        self.generations.append(new_generation)

        self.current_generation_number += 1


    



    



