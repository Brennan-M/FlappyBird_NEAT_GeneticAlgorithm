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


def main(num_species, generations, initial_organisms, organisms):
    
    init_species = Species(initial_organisms)
    
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

            if current_species.check_extinct():
                print("\n\n*** \t *** Exctintion Event! *** \t ***")
                break
            
            if current_species.current_generation_number == 0:
                print("\n\n*** \t *** Species Survives! Time to expand! *** \t ***")
                current_species.expand_population(organisms)
                
            else:
                species[species_index].selection()
                species[species_index].replication()

        new_species = Species(initial_organisms, species_ID=species_index)
        species.append(new_species)
        print("\n\n")


if __name__ == "__main__":
    
    num_species = 100
    generations = 10000
    
    initial_organisms = 2
    organisms = 10  # number of neural nets per generation - NOTE: Must be even number
    main(num_species, generations, initial_organisms, organisms)