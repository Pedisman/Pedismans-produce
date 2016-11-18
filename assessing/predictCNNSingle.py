import os
import tensorflow as tf

import numpy as np

from tensorflow.examples.tutorials.mnist import input_data
data = input_data.read_data_sets("/tmp/data/", one_hot=True)

#### load image
import cv2

filename = 'digit4.PNG'
image = cv2.imread(filename, 0)

cv2.imshow('yo', image)
cv2.waitKey(0)

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
		sum += probs[0][i]
	print(sum)

MINIMUM_CONTOUR_AREA = 10

def process(image, Nshape = (28, 28)):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)[1]
    #closing = cv2.dilate(thresh, (5,5), iterations = 40)
    #closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, (5, 5), iterations=60)
    __, contours, im2 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largestContour = contours[0]
    for con in contours:
        if (cv2.contourArea(con) > MINIMUM_CONTOUR_AREA):
            if (cv2.contourArea(con) > cv2.contourArea(largestContour)):
                largestContour = con

    x, y, w, h = cv2.boundingRect(largestContour)

    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    ROI = thresh[y:y + h , x:x + w]
    #scaledROI = cv2.resize(ROI, Nshape)
    scaledROI = cv2.resize(thresh, Nshape)

    cv2.imshow("scaledROI", scaledROI)
    cv2.waitKey(0)

    return scaledROI.flatten()

def predictTheThang(image):
	prediction = tf.argmax(y, 1)
	print("predictions", prediction.eval(feed_dict={x: image.reshape(1,784), keep_prob: 1.0}, session=sess))
	probabilities = y
	#note to get a single output need to 
	prob = probabilities.eval(feed_dict={x: image.reshape(1,784), keep_prob: 1.0}, session=sess)
	print("probabilities", prob[0])
	print("probabilities", prob[0][7])
	estimationProbs(prob)
	
	#cv2.imshow('test', data.test.images[0].reshape(28,28))
	#cv2.waitKey(0)	

with tf.Session() as sess:
     # Restore variables from disk.
	saver.restore(sess, "../tensorflow-mnist/mnist/data/convolutional2.ckpt")
	print("Model restored.")
	predictTheThang(process(image))
	#predictTheThang(data.test.images[800])
	'''
	prediction = tf.argmax(y, 1)
	print(data.test.labels[6000])
	print("predictions", prediction.eval(feed_dict={x: data.test.images[6000].reshape(1,784), keep_prob: 1.0}, session=sess))
	probabilities = y
	#note to get a single output need to 
	prob = probabilities.eval(feed_dict={x: data.test.images[6000].reshape(1,784), keep_prob: 1.0}, session=sess)
	print("probabilities", prob[0])
	print("probabilities", prob[0][7])
	estimationProbs(prob)
	'''
	#print(sess.run(accuracy, feed_dict={x: data.test.images, y_: data.test.labels}))
