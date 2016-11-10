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


    def pretty_print_s_id(self, s_id):
        print "\n"
        print "===================="
        print "===  Species:", s_id, " ==="
        print "===================="
        print "\n"

