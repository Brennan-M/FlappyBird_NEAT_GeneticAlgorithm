from modules.species import Species

"""
Engine
------

This is the engine.

Creates a new species, where each species has the potential for X generations, and each generation contains Y networks.

To expedite the learning process, only 2 networks per generation are started with. 

If all networks result in a fitness of 0, the species goes extinct and a new species is created with newly randomized neural nets.

The process is:

    1. Create species
    2. Generate fitness (have each network in the current generation of the current species play the game)
    3. Check if all fitnesses are 0.
        a. If all fitness = 0, species goes extinct.
        b. Else,
            i. Selection on species of fittest network
            ii. Replicate (with mutation) the fittest networks

"""


def main(num_species, generations, organisms):
    
    init_species = Species(organisms)
    
    species = [init_species]

    for species_index in range(num_species):
        print("\n*$----------------=================================----------------$*")
        print("*$=================================================================$*")
        print("\t\t\t   Species {}".format(species_index))
        print("*$=================================================================$*")
        print("*$----------------=================================----------------$*")
        current_species = species[species_index]

        for generation in range(generations):
            current_species.generate_fitness()
            current_species.selection()
            current_species.replication()

        new_species = Species(organisms, species_ID=species_index)
        species.append(new_species)
        print("\n\n")


if __name__ == "__main__":
    
    num_species = 100
    generations = 10000
    
    
    organisms = 8  # number of neural nets per generation - NOTE: Must be even number
    main(num_species, generations, organisms)


