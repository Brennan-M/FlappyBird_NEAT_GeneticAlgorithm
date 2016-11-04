import numpy as np
import random, math
from datetime import datetime
import tensorflow as tf


class Interface:

    def __init__(self, net_ID, gen_ID, frequency=15):
        self.network_ID = net_ID
        self.generation_ID = gen_ID
        self.fitness = None
        
        random.seed(datetime.now())

        self.frequency = frequency

        # Set up tensor flow
        self._init_TF_()


    def _init_TF_(self):
        """
            What a mess...
        """
        self.input_layer_size = 6
        self.output_layer_size = 1

        # Initialize placeholders for inputs and outputs
        self.x = tf.placeholder(tf.float32, [None, self.input_layer_size])
        self.y = tf.placeholder(tf.int32, shape=(self.output_layer_size))

        # Initialize weights and biases
        self.Weights = tf.Variable(tf.truncated_normal([self.input_layer_size, self.output_layer_size],
                        stddev=1.0 / math.sqrt(float(self.input_layer_size))),
                        name='weights')

        self.biases = tf.Variable(tf.zeros([self.output_layer_size], 
                        name='biases'))

        # Initialize hidden layer
        self.hidden1 = tf.nn.relu(tf.matmul(images, weights) + biases)

        # Initialize logics
        self.logits = tf.matmul(self.hidden1, weights) + biases

        #self.y = tf.nn.softmax(tf.matmul(self.x, self.W) + self.b)
        #print("\n\t\t**self.y: {}".format(self.y))

        init = tf.initialize_all_variables()
        sess = tf.Session()
        sess.run(init)



    def set_fitness(self, fitness):
        self.fitness = fitness


    def mutate(self):
        """
            Simulates a mutation of the weights or nodes of a neural network.
            Since our 'prediction' is simply pulled from a binomial distribution (I think...),
                then our simulated weight is the frequency (self.frequency)
            To mutate, we roll a 3-sided die. 
                If 0, increment the frequency by 1,
                elif 1, decrement by 1
                else, no mutation.
        """
        coin_flip = np.random.randint(3)

        if coin_flip == 0:
            return self.frequency + 1
        elif coin_flip == 1:
            return self.frequency - 1
        else:
            return self.frequency



    def update(self, player, pipes):
        self.player_top = player.top
        self.player_bottom = player.bottom

        self.pipes_top = pipes.top
        self.pipes_bottom = pipes.bottom
        self.pipes_left = pipes.left
        self.pipes_right = pipes.right

        # Update tensor_flow
        self._update_TF()

    def _update_TF(self):
        y_ = tf.placeholder(tf.float32, [None, self.output_layer_size])
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(self.y), reduction_indices=[1]))


    def predict(self):
        random_output = np.random.randint(self.frequency)
        if random_output == 0:
            return True
        else:
            return False
        



