import os
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
data = input_data.read_data_sets("/tmp/data/", one_hot=True)

# model
import model
with tf.variable_scope("convolutional"):
    x = tf.placeholder("float", [None, 784])
    y, variables, keep_prob = model.convolutional(x)

# train
y_ = tf.placeholder("float", [None, 10])
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

saver = tf.train.Saver(variables)
init = tf.initialize_all_variables()
with tf.Session() as sess:
     # Restore variables from disk.
	saver.restore(sess, "data/convolutional.ckpt")
	print("Model restored.")
	print(sess.run(accuracy, feed_dict={x: data.test.images, y_: data.test.labels, keep_prob: 1.0}))
