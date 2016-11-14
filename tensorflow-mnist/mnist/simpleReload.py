import os
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
data = input_data.read_data_sets("/tmp/data/", one_hot=True)

# model
import model
with tf.variable_scope("simple"):
    x = tf.placeholder("float", [None, 784])
    y, variables = model.simple(x)

# train
y_ = tf.placeholder("float", [None, 10])
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))

#cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_conv, y_))
#train using the adam optimizer rather than gradient descent
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

saver = tf.train.Saver(variables)
init = tf.initialize_all_variables()
with tf.Session() as sess:
     # Restore variables from disk.
	saver.restore(sess, "data/simple.ckpt")
	print("Model restored.")
	print(sess.run(accuracy, feed_dict={x: data.test.images, y_: data.test.labels}))
