from modules.species import Species

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