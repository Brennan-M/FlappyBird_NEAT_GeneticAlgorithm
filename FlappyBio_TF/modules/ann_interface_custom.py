import numpy as np
import math, random
from sklearn import preprocessing
from sklearn.preprocessing import normalize
from datetime import datetime
import tensorflow as tf
from copy import deepcopy

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

------------------------------------------------------------------------------------------------
TF Slicing based on variable
    http://stackoverflow.com/questions/34002591/tensorflow-slicing-based-on-variable

------------------------------------------------------------------------------------------------
TF math
    https://www.tensorflow.org/versions/r0.11/api_docs/python/math_ops.html
"""


MUTATION_RATE = 0.5
topology = [8, 1]
random.seed(datetime.now())


class Network:

    def __init__(self, ID, genes=None, mutation=False):
        
        self.max_neurons_per_hidden_layer = 20
        
        self.topology = topology
        self.input_layer_size = topology[0]
        self.output_layer_size = topology[-1]

        
        self.fitness = None

        try:
            self.num_hidden_layers = len(topology[1:-1])
            self.hidden_layers = []
        except:
            self.num_hidden_layers = 0

        
        self._init_(ID, topology[0], topology[-1], genes, mutation)
            
            

    def _init_(self, ID, input_size, output_size, inhereted_genes, mutations, activation="relu"):
        
        # Place Holders
        self.x = tf.placeholder(tf.float32, shape=[1, input_size])

        # Variables
        if inhereted_genes:
            parent_W = inhereted_genes[1]
            parent_b = inhereted_genes[2]

            self.W = tf.Variable(tf.random_normal((input_size, output_size)))
            self.b = tf.Variable(tf.zeros(output_size))

            copy_W = self.W.assign(parent_W)
            copy_b = self.b.assign(parent_b)
                    
        else:
            self.W = tf.Variable(tf.random_normal((input_size, output_size)))
            self.b = tf.Variable(tf.zeros(output_size))
        
        self.network_ID = ID["network"]
        self.generation_ID = ID["generation"]
        self.species_ID = ID["species"]


        # Initialize output activation function
        if activation is "relu":
            self.y = tf.nn.relu(tf.matmul(self.x, self.W) + self.b)
        elif activation is "sigmoid":
            self.y = tf.sigmoid(tf.matmul(self.x, self.W) + self.b)
        

        # Initialize to true for first flap to start the game
        self.output = True


        # Initialize TF variables above
        init_op = tf.initialize_all_variables()
        self.sess = tf.Session()
        self.sess.run(init_op)

        if mutations:
            self.mutate()


    def close_tensor_flow_session(self):
        self.sess.close()
      
        
    def copy(self):
        return (deepcopy(topology), self.W, self.b)


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

        #print("Raw output: {}".format(Z))
        if Z >= 0.5:
            self.output = True
        else:
            self.output = False
        #print("Flap: {}\n".format(self.output))
     

    

    def set_fitness(self, fitness):
        self.fitness = fitness


    def mutate(self):
        
        mutations = [self.mutate_W(), self.mutate_b()]
        mutate = random.uniform(0, 1)

        if mutate <= MUTATION_RATE:
            mutate_index = np.random.randint(2)
            if mutate_index == 0:
                print("Mutate W!")
                mutations[mutate_index]

            elif mutate_index == 1:
                print("Mutate b!")
                mutations[mutate_index]

        
        
        

    def mutate_W(self):
        # Declare new mutation variables
        delta_w = tf.constant(0.05)

        mutate_index = np.random.randint(self.W.get_shape()[0]+1)

        for index in range(self.W.get_shape()[0]):
            w = self.W[index]
            tu = tf.add(delta_w, w)
            if index == mutate_index:
                print("w to mutate: {}".format(self.sess.run(w)))
                new_w = w.assign(tu)
                self.sess.run(new_w)
                print("w mutated: {}".format(self.sess.run(w)))


    def mutate_b(self):
        # Declare new mutation variables
        delta_b = tf.constant(0.05)

        mutate_index = np.random.randint(self.b.get_shape()[0]+1)

        for index in range(self.b.get_shape()[0]):
            b = self.b[index]
            tu = tf.add(delta_b, b)
            if index == mutate_index:
                print("b to mutate: {}".format(self.sess.run(b)))
                new_b = b.assign(tu)
                self.sess.run(new_b)
                print("b mutated: {}".format(self.sess.run(b)))


    def mutate_hidden_layer(self):
        pass


    def update(self, player, Upipes, Lpipes):
        
        X = np.zeros(self.input_layer_size)
        X[0] = player.top
        X[1] = player.bottom
        X[2] = player.left
        X[3] = player.right
        X[4] = Upipes.bottom
        X[5] = Lpipes.top
        X[6] = Upipes.left
        X[7] = Upipes.right

        self.feed_forward(X)



    def predict(self):
        return self.output


    def set_fitness(self, fitness):
        self.fitness = fitness







