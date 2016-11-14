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
#cross entropy
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))
#train using the adam optimizer rather than gradient descent
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

saver = tf.train.Saver(variables)
init = tf.initialize_all_variables()
with tf.Session() as sess:
	sess.run(init)
	for i in range(300):
		batch = data.train.next_batch(50)
		if i%100 == 0:
			train_accuracy = accuracy.eval(feed_dict={ x:batch[0], y_: batch[1], keep_prob: 1.0})
			print("step %d, training accuracy %g"%(i, train_accuracy))
		train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

	#keep probability controls the dropout rate
	print("test accuracy %g"%accuracy.eval(feed_dict={ x: data.test.images, y_: data.test.labels, keep_prob: 1.0}))
	path = saver.save(sess, os.path.join(os.path.dirname(__file__), "data/convolutional2.ckpt"))
	print("Saved:", path)
