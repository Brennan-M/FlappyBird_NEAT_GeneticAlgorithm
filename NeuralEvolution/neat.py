from NeuralEvolution.species import Species
from NeuralEvolution.network import mate

INITIAL_FITNESS = -10**3

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

        survivor_to_cross = []
        for s_id in xrange(self.num_species):
            s = self.species[s_id]
            self.pretty_print_s_id(s_id)
            s.evolve()

            survivor = self.select_survivors(s_id)
            #survivor_network = self.species[s_id].generations[survivor["gen_id"]][survivor["network_num"]]
            #print("----- SURVIVOR: {0}-{1}\tFITNESS: {2}\tGENES: {3}".format(survivor["gen_id"], survivor["network_num"], survivor_network.fitness, survivor_network.get_genes()))
            survivor_to_cross.append(survivor)

            if len(survivor_to_cross) == 2 and s_id < (self.num_species - 1):
                #print("------ ALL SURVIVORS: {0}".format(survivor_to_cross))
                # Seed the next species with some splicing of the best
                inherited_genes = mate(survivor_to_cross[0]["network"], 
                                       survivor_to_cross[1]["network"])
                self.species[s_id + 1] = Species(self.organism_topology,
                    self.num_generations_per_spec,
                    self.num_networks_per_gen,
                    (s_id + 1),
                    inherited_genes)
                survivor_to_cross = []


    def select_survivors(self, s_id):
        species = self.species[s_id]
        # Go through each generation, searching for the fittest network
        top_fitness = INITIAL_FITNESS
        for gen in xrange(self.num_generations_per_spec):
            # Fing the best network of a generation
            net = sorted(species.generations[gen], key=lambda k: species.generations[gen][k].fitness, reverse=True)[0]

            # If this is the fittest network we've seen of this species,
            # then update our top survivor
            if species.generations[gen][net].fitness > top_fitness:
                top_survivor_gen_id = gen; top_survivor_net_id = net
                top_fitness = species.generations[gen][net].fitness
                top_network = species.generations[gen][net]
                #print(">>>>> GENERATION: {0}\tNETWORK: {1}".format(top_survivor_gen_id, top_survivor_net_id))
        
        return{"s_id": s_id, "gen_id": top_survivor_gen_id, "network_num": top_survivor_net_id, "network": top_network}


    def pretty_print_s_id(self, s_id):
        print "\n"
        print "===================="
        print "===  Species:", s_id, " ==="
        print "===================="
        print "\n"

