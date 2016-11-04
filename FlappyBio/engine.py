import modules.flappy as flpy
from modules.ann_interface import *
import numpy as np

class Environment:

    def __init__(self, networks_per_generation=10):

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
            parent_gen.append(Interface(network_ID, generation_ID))

        self.generations.append(parent_gen)


    def generate_fitness(self):
        """
            Generates the fitness for each network in the generation.
            The fitness is a measured by each networks performance 
                (i.e. the score it achieves playing Flappy Birds)
        """
        current_generation = self.generations[self.current_generation_number]
        print("Generation {}".format(self.current_generation_number))

        for network in current_generation:
            print("\tNetwork {}\tFlap Frequency: {}".format(network.network_ID, network.frequency))
            results = flpy.main(network)
            fitness_score = results['score']
            network.set_fitness(fitness_score)

            print("Fitness Score: {}".format(fitness_score))

        
        


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

        for network in generations:
            
            if network.fitness > max_fitness:
                top_network = network

        print("\tTop Network: {}\tFitness: {}".format(top_network.network_ID, top_network.fitness))
        self.top_networks.append(top_network)


    def replication(self):
        """

        """
        print("\n")
        print("\t=====================")
        print("\t     Replication     ")
        print("\t=====================")
        top_network = self.top_networks[self.current_generation_number]

        child_generation = []
        for new_network_ID in range(self.networks_per_generation):
            mutations = top_network.mutate()
            new_network = Interface(new_network_ID, self.current_generation_number+1, mutations)
            child_generation.append(new_network)

        self.generations.append(child_generation)

        self.current_generation_number += 1
        


def main():
    scores = []
    
    environment = Environment(2)

    for generation in range(10):

        environment.generate_fitness()
        environment.selection()
        environment.replication()

    

if __name__ == "__main__":
    main()