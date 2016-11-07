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

------------------------------------------------------------------------------------------------
TF Slicing based on variable
    http://stackoverflow.com/questions/34002591/tensorflow-slicing-based-on-variable

------------------------------------------------------------------------------------------------
TF math
    https://www.tensorflow.org/versions/r0.11/api_docs/python/math_ops.html
"""

def run(X):   
    feed_dict = {self.x: X} 
    
    with tf.Session() as sess:
        Z = sess.run(y, feed_dict=feed_dict)
    
       
input_size = 8
output_size = 1

# Place Holders
x = tf.placeholder(tf.float32, shape=[1, input_size])


# Variables
W = tf.Variable(tf.random_normal((input_size, output_size)))
b = tf.Variable(tf.zeros(output_size))

y = tf.nn.relu(tf.matmul(x, W) + b)



#
delta_W = tf.Variable(tf.random_normal((input_size, output_size)))
new_W = tf.add(delta_W, W)


# Initialize variables
init_op = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init_op)

print("W: {}".format(W))
print("W.get_shape(): {}".format(W.get_shape()))

print("\nBefore Mutation")
for i in range(8):
    w = W[i]
    print("w: {}".format(sess.run(w)))

print("\nMutation...")
for i in range(8):
    delta_w = tf.constant(0.5)
    w = W[i]

    tu = tf.add(delta_w, w)
    if i == 0:
        print("w to mutate: {}".format(w))
        new_w = w.assign(tu)
        sess.run(new_w)
        #print("new_w: {}".format(w))
        #with sess.as_default():
        #    w = sess.run(tu)
            

print("\nPost mutation...")
for i in range(8):
    w = W[i]
    print("w: {}".format(sess.run(w)))
# with tf.Session() as sess:
#     Z = sess.run(new_W)


print("W.get_shape(): {}".format(W.get_shape()[1]))






    
    
         
    

   