import numpy as np
import math, random
from sklearn import preprocessing
from sklearn.preprocessing import normalize
from datetime import datetime
import tensorflow as tf
from copy import deepcopy


random.seed(datetime.now())


class Network:

    def __init__(self, network_info, inherit_parent_genes=False, inherited_genes=None):
        
        self.tensorflow_session = tf.Session()

        # Neural Net meta data
        self.network_number = network_info["network"]
        self.generation_number = network_info["generation"]
        self.species_number = network_info["species"]

        # Neural Net structure information
        self.mutation_rate = 0.5
        self.topology = (6, 1)
        self.num_input_neurons = self.topology[0]
        self.num_output_neurons = self.topology[1]
        self.max_neurons_per_hidden_layer = 20
        self.num_hidden_layers = 1 # May increase based on mutations

        # Neural Net values
        self.fitness = 0
        self.x = tf.placeholder(tf.float32, shape=[1, self.num_input_neurons])
        self.W = tf.Variable(
                    tf.random_normal((self.num_input_neurons, self.num_output_neurons))
                 )
        self.b = tf.Variable(
                    tf.zeros(self.num_output_neurons)
                 ) 

        if (not inherit_parent_genes):

            initial_var_values = tf.initialize_variables([self.W, self.b])
            self.tensorflow_session.run(initial_var_values)

        # else: # Inherit Parent Genes

        #     update_W = tf.add(self.W, inherited_genes[1])
        #     update_b = tf.add(self.b, inherited_genes[2])
            
        #     new_W = tf.assign(self.W, update_W)
        #     new_b = tf.assign(self.b, update_b)  
            
        #     initial_var_values = tf.initialize_variables([self.W, self.b])
        #     self.sess.run(initial_var_values)

        #     self.sess.run(new_W)
        #     self.sess.run(new_b)

        # Could be a different activation function here
        self.y = tf.nn.relu(tf.matmul(self.x, self.W) + self.b) # Our Model

    
    def close_tensor_flow_session(self):
        self.tensorflow_session.close()
      
        
    # def copy(self):
    #     return (deepcopy(topology), self.W, self.b)


    def norm_input(self, X):
        return preprocessing.scale(X)


    def predict(self, player_inputs, upper_pipe_inputs, lower_pipe_inputs, normalize_input=True):
        X = np.zeros(self.num_input_neurons)
        X[0] = player_inputs[0]
        X[1] = player_inputs[1]
        X[2] = upper_pipe_inputs[0]['y']
        X[3] = upper_pipe_inputs[0]['x']
        X[4] = upper_pipe_inputs[1]['x']
        X[5] = lower_pipe_inputs[0]['y']

        if normalize_input:
            X = self.norm_input(X)
        X = X.reshape(1, len(X))
        
    
        feed_dict = {self.x : X}
        Z = self.tensorflow_session.run(self.y, feed_dict)

        if Z >= 0.5:
            return True
        else:
            return False


    def set_fitness(self, fitness):
        self.fitness = fitness



    # def mutate(self):
        
    #     mutations = [self.mutate_W(), self.mutate_b()]
    #     mutate = random.uniform(0, 1)

    #     if mutate <= MUTATION_RATE:
    #         mutate_index = np.random.randint(2)
    #         if mutate_index == 0:
    #             print("\tMutate W!")
    #             mutations[mutate_index]

    #         elif mutate_index == 1:
    #             print("\tMutate b!")
    #             mutations[mutate_index]

    
        

    # def mutate_W(self):
    #     # Declare new mutation variables
    #     if np.random.randint(2) == 0:
    #         delta_w = tf.constant(0.1)
    #     else:
    #         delta_w = tf.constant(-0.1)

    #     mutate_index = np.random.randint(self.W.get_shape()[0]+1)


    #     for index in range(self.W.get_shape()[0]):
    #         w = self.W[index]
            
            
    #         if index == mutate_index:
    #             tu = tf.add(w, delta_w)
    #             update = w.assign(tu)
    #             init_op = tf.initialize_variables([tu])
    #             self.sess.run(init_op)
    #             self.sess.run(update)

    #             print("\n\t\tw**: {}".format(self.sess.run(w)))    
    #             # # new_w = tf.assign(tu, w)
    #             # # self.sess.run(new_w)
    #             # new_w = w.assign(tu)
    #             # self.sess.run(tu)
    #             print("\t\t\tw**: {}".format(self.sess.run(w)))

    #         print("\n\t\tw: {}".format(self.sess.run(w)))

    # def mutate_b(self):
    #     # Declare new mutation variables
    #     if np.random.randint(2) == 0:
    #         delta_b = tf.constant(0.1)
    #     else:
    #         delta_b = tf.constant(-0.1)

    #     mutate_index = np.random.randint(self.b.get_shape()[0]+1)

    #     for index in range(self.b.get_shape()[0]):
    #         b = self.b[index]
    #         tu = tf.add(delta_b, b)
    #         if index == mutate_index:
    #             print("\n\t\tb before mtuation: {}".format(self.sess.run(b)))
    #             #new_b = tf.assign(tu, b)
    #             #self.sess.run(new_b)
    #             self.sess.run(tu)
    #             print("\t\tb after mtuation: {}".format(self.sess.run(b)))


    # def mutate_hidden_layer(self):
    #     pass







