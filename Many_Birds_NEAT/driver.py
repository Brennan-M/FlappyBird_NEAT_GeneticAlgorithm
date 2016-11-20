from FlapPyBird.flappy import FlappyBirdApp
from config.config import *
from NEAT.neural_network import Neural_Network
import numpy as np

INPUTS = 10
OUTPUTS = 1

class Environment(object):
    def __init__(self):
        # Create parent generation
        self.generations = []
        initial_topology = [INPUTS, OUTPUTS]
        self.generations.append([Neural_Network(initial_topology) for _ in range(POPULATION)])

    def start(self):

        # Create 
        for generation_index in range(GENERATIONS):
            current_generation = self.generations[generation_index]
            
            """ FITNESS """
            self.fitness(current_generation)

            """ SELECTION """
            self.selection(current_generation)

            """ REPLICATION """
            self.replication(current_generation)

        

    def fitness(self, current_generation):

        # Play game and get results
        flappy_Bio = FlappyBirdApp(current_generation)
        flappy_Bio.play()
        results = flappy_Bio.crash_info

        # Calculate fitness
        

        self.fitness_values = []
        self.network_index_dict = {}
        for index, result in enumerate(results):
            network = result['network']
            self.network_index_dict[index] = network

            distance = result['distance']
            energy = result['energy']
            
            fitness = distance - energy*0.5
            fitness = -1 if fitness == 0 else fitness

            self.fitness_values.append((index, fitness))




    def selection(self, current_generation):
        dtype = [('network_index', int), ('fitness', int)]
        self.fitnesses = np.array(self.fitness_values, dtype=dtype)

        sorted_fitness_indices = np.sort(self.fitnesses, order='fitness')[::-1]

        self.top_networks = []
        for top_fitness_indices in sorted_fitness_indices[:int(len(sorted_fitness_indices)/2)]:
            self.top_networks.append(self.network_index_dict[top_fitness_indices[0]])

        
    def replication(self, current_generation):
        new_generation = []
        for top_network in self.top_networks:
            progeny = []
            for _ in range(2):
                topology, genes = top_network.copy_genes()
                new_network = Neural_Network(topology, genes)
                progeny.append(new_network)

            new_generation += progeny



        self.generations.append(new_generation)

            
            




if __name__ == "__main__":
    world = Environment()
    world.start()
        
