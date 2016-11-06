import numpy as np
import math
from sklearn import preprocessing
from sklearn.preprocessing import normalize
import tensorflow as tf
sess = tf.InteractiveSession()

"""
Network Class
=============
------------------------------------------------------------------------------------------------

https://www.tensorflow.org/versions/r0.11/tutorials/mnist/tf/index.html#inputs-and-placeholders

------------------------------------------------------------------------------------------------
.run()  
    https://www.tensorflow.org/versions/r0.11/api_docs/python/client.html

------------------------------------------------------------------------------------------------
Assign new value to variable in tf
    http://stackoverflow.com/questions/34220532/how-to-assign-value-to-a-tensorflow-variable

------------------------------------------------------------------------------------------------
Discussion on indexing tf variables
    https://github.com/tensorflow/tensorflow/issues/418
    https://github.com/tensorflow/tensorflow/issues/206

------------------------------------------------------------------------------------------------
Assigning new values to variables
    http://stackoverflow.com/questions/35148121/assign-op-in-tensorflow-what-is-the-return-value

------------------------------------------------------------------------------------------------
Constants, Sequences, and Random Values
    https://www.tensorflow.org/versions/r0.11/api_docs/python/constant_op.html#range

------------------------------------------------------------------------------------------------
TF py code example
    https://github.com/tensorflow/tensorflow/blob/r0.11/tensorflow/models/image/cifar10/cifar10_input.py

------------------------------------------------------------------------------------------------
How To Standardize Data for Neural Networks
    https://visualstudiomagazine.com/articles/2014/01/01/how-to-standardize-data-for-neural-networks.aspx
"""

class Network:

    def __init__(self, topology, copy=False, mutation=False):
        
        self.max_neurons_per_hidden_layer = 20

        self.topology = topology
        self.input_layer_size = topology[0]
        self.output_layer_size = topology[-1]

        try:
            self.num_hidden_layers = len(topology[1:-1])
            self.hidden_layers = []
        except:
            self.num_hidden_layers = 0


        if copy:
            self.__copy__()
        
        else:
            self._init_(topology[0], topology[-1], mutations=mutation)
            
            

    def _init_(self, input_size, output_size, activation="relu", mutations=None):
        
        # Place Holders
        self.x = tf.placeholder(tf.float32, shape=[1, input_size])

        # Variables
        if not mutations:
            self.W = tf.Variable(tf.random_normal((input_size, output_size)))
            self.b = tf.Variable(tf.zeros(output_size))
        else:
            if mutations[0] is 'W':
                self.W = tf.Variable(tf.random_normal((input_size, output_size)))
                self.b = mutations[1]
            elif mutations[0] is 'b':
                self.W = mutations[1]
                self.b = tf.Variable(tf.zeros(output_size))


        # Initialize output 
        if activation is "relu":
            self.y = tf.nn.relu(tf.matmul(self.x, self.W) + self.b)
        elif activation is "sigmoid":
            self.y = tf.sigmoid(tf.matmul(self.x, self.W) + self.b)
        

        # Initialize to true for first flap
        self.output = True
 
        # Initialize variables
        init_op = tf.initialize_all_variables()

        self.sess = tf.Session()
        self.sess.run(init_op)

      
        

    def __copy__(self):
        pass


    def norm_input(self, X, norm_type='other'):
        if norm_type is 'gauss':
            norm1 = X / np.linalg.norm(X)
            return normalize(X[:,np.newaxis], axis=0).ravel()

        # This one seems to work better, for now
        elif norm_type is 'other':
            norm1 = preprocessing.scale(X)
            return norm1



    def feed_forward(self, X, normalize_input=True):
        # Normalize input

        if normalize_input:
            X_norm = self.norm_input(X)
            y = X_norm.reshape(1, len(X_norm))
        else:
            y = X.reshape(1, len(X))
        
        
        feed_dict = {self.x: y}
             
        with tf.Session() as sess:
            Z = self.sess.run(self.y, feed_dict=feed_dict)

        print("Raw output: {}".format(Z))
        if Z >= 0.5:
            self.output = True
        else:
            self.output = False
        print("Flap: {}\n".format(self.output))
     

    

    def set_fitness(self, fitness):
        self.fitness = fitness


    def mutate(self):
        #network_elements = [self.W, self.b]

        rand_index = np.random.randint(2)

        if rand_index == 0:
            mutations = ["W", self.b]
        elif rand_index == 1:
            mutations = ["b", self.W]
        
        return mutations

    # def mutate(self):
        
        # network_elements = [self.W1, self.W2, self.b1, self.b2, self.hidden_layer_size]
        # elements_size = len(network_elements)

        # mutation_index = np.random.randint(elements_size)
        
        # mutation_element = network_elements[mutation_index]

        # # Weight matrix mutation
        # if mutation_index == 0 or mutation_index == 1:
        #     print("\n\tMutation to Weight Matrix.\n")
        #     self.mutate_W(mutation_element)

        # elif mutation_index == 2 or mutation_index == 3:
        #     print("\n\tMutation to Bias.\n")
        #     self.mutate_b(mutation_element)

        # elif mutation_index == 4:
        #     print("\n\tMutation to Hidden Layer.\n")
        #     self.mutate_hidden_layer(self.W1, self.W2, mutation_element)
        
        # return network_elements



    # def mutate_W(self, element):
    #     num_rows = len(element)
    #     num_cols = len(element[0])
        
    #     mutation_row = np.random.randint(num_rows)
    #     mutation_col = np.random.randint(num_cols)
    #     #print("Mutation at {},{}: {}".format(mutation_row, mutation_col, element[mutation_row][mutation_col]))
        
    #     mutation = np.random.randn(1) * 50
    #     #print("Mutation: {}".format(mutation))
    #     element[mutation_row][mutation_col] += mutation
    #     #print("Post Mutation at {},{}: {}".format(mutation_row, mutation_col, element[mutation_row][mutation_col]))
        

    # def mutate_b(self, element):
    #     mutation = np.random.randn(1) * 50
    #     element += mutation
        

    # def mutate_hidden_layer(self, W1, W2, element):

    #     if np.random.randn(1) >= 0:
    #         node_change = 1
    #     else:
    #         if element > 1:
    #             node_change = -1

    #     element += node_change

        
    #     # Update W1
    #     W1_num_cols = len(W1[0])
    #     new_W1 = np.random.randn(element, W1_num_cols)
    #     for row_i, row in enumerate(new_W1[:element]):
    #         for col_i, ele in enumerate(row):
    #             new_W1[row_i][col_i] = ele

    #     W1 = new_W1


    #     # Update W2
    #     new_W2 = np.random.randn(1, element) * 50
    #     for index, col in enumerate(new_W2[0][:element]):
    #         new_W2[0][index] = col
            
    #     W2 = new_W2
        
                
