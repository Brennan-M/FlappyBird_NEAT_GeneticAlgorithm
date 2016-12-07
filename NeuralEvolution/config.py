# Configurations for NEAT



INPUT_NEURONS = 10
OUTPUT_NEURONS = 1
POPULATION = 50
STAGNATED_SPECIES_THRESHOLD = 2000
STAGNATIONS_ALLOWED = 2
CROSSOVER_CHANCE = 0.75
WEAK_SPECIES_THRESHOLD = 3
ACTIVATION_THRESHOLD = 0.5
WEIGHT_MUTATION_RATE = 0.8
UNIFORM_WEIGHT_MUTATION_RATE = 0.9
ADD_GENE_MUTATION = 0.05
ADD_NODE_MUTATION = 0.03
ENABLE_GENE_MUTATION_RATE = 0.2 # 0.0 means no reenabling of genes possible



# NOT USING AT THE MOMENT

# Speciation Constants
C1 = 2.0        # Excess weight
C2 = 2.0        # Disjoint weight
C3 = 0.4        # Weight average weight
DELTA_T = 0.5   # New species threshold

DISABLE_INHERITED_GENE_CHANCE = 0.75


# ------------------------------------------
STEP_SIZE = 0.1
