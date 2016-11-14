import os
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
data = input_data.read_data_sets("/tmp/data/", one_hot=True)

import sys
sys.path.append('../tensorflow-mnist/mnist')

# model
import model
with tf.variable_scope("convolutional"):
    x = tf.placeholder("float", [None, 784])
    y, variables, keep_prob = model.convolutional(x)

saver = tf.train.Saver(variables)
init = tf.initialize_all_variables()

print(data.test.images[0])

def estimationProbs(probs):
	sum = 0.0
	for i in range(0,10):
		sum += prob[0][i]
	print(sum)

with tf.Session() as sess:
     # Restore variables from disk.
	saver.restore(sess, "../tensorflow-mnist/mnist/data/convolutional.ckpt")
	print("Model restored.")
	prediction = tf.argmax(y, 1)
	print(data.test.labels[6000])
	print("predictions", prediction.eval(feed_dict={x: data.test.images[6000].reshape(1,784), keep_prob: 1.0}, session=sess))
	probabilities = y
	#note to get a single output need to 
	prob = probabilities.eval(feed_dict={x: data.test.images[6000].reshape(1,784), keep_prob: 1.0}, session=sess)
	print("probabilities", prob[0])
	print("probabilities", prob[0][7])
	estimationProbs(prob)
	#print(sess.run(accuracy, feed_dict={x: data.test.images, y_: data.test.labels}))
