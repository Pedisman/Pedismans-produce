import os
import tensorflow as tf
import cv2

from tensorflow.examples.tutorials.mnist import input_data
data = input_data.read_data_sets("/tmp/data/", one_hot=True)

print (data.test.images[0])

showImage = data.test.images[0].reshape((28,28))

cv2.imshow('image', showImage)

cv2.waitKey(0)
