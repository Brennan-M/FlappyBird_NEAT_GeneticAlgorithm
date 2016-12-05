"""
     http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf
"""

import numpy as np

GENERATIONS = 10
POPULATION = 100
C1 = 1.0
C2 = 1.0
C3 = 0.4
connection_weight_mutation_chance = 0.8
chance_of_each_weight_uniform_mutation = 0.9
chance_of_each_weight_randomly_mutated = 0.1
chance_disable_inherited_gene = 0.75
chance_mutation_NO_crossover = 0.25
chance_interspecies_mating = 0.001
SMALL_POPULATION_new_node = 0.03
SMALL_POPULATION_new_link_mutation = 0.05
LARGE_POPULATION_new_link_mutation = 0.3
sigm = lambda x: 1/(1+np.exp(-4.9*x))
