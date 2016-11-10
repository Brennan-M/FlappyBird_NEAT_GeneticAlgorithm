from NeuralEvolution.species import Species



class NEAT(object):


    def __init__(self,
                 topology,
                 num_species=5, 
                 num_generations_per_spec=100,
                 num_networks_per_gen=10):

        self.num_species = num_species
        self.num_generations_per_spec = num_generations_per_spec
        self.num_networks_per_gen = num_networks_per_gen
        self.organism_topology = topology

        self.species = {}


    def start_evolutionary_process(self):
        for s_id in xrange(self.num_species):
            new_species = Species(self.organism_topology,
                                  self.num_generations_per_spec,
                                  self.num_networks_per_gen,
                                  s_id)
            self.species[s_id] = new_species

        for s_id, s in self.species.items():
            self.pretty_print_s_id(s_id)
            s.evolve()

            self.crossover(s_id)

    def crossover(self, s_id):
        # Find the best performing networks across generations of this species
        species = self.species[s_id]
        for gen in xrange(self.num_generations_per_spec):
            sorted_network_ids = sorted(species.generations[gen], key=lambda k: species.generations[gen][k].fitness, reverse=True)
            top_survivor = sorted_network_ids[0]
            fitness = species.generations[gen][top_survivor].fitness
            genes = species.generations[gen][top_survivor].get_genes()

            print("top survivor: {0}\tfitness: {1}\tgenes: {2}".format(top_survivor, fitness, genes))


    def pretty_print_s_id(self, s_id):
        print "\n"
        print "===================="
        print "===  Species:", s_id, " ==="
        print "===================="
        print "\n"

