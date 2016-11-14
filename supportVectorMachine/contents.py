# import necessary packages
import cv2
import numpy as np

imageShape = (28,28)

imageFile = "./images.dat.npy"
featureFile = "./features.dat.npy"
targetFile = "./targets.dat.npy"

features = np.load(featureFile)
images = np.load(imageFile)
target = np.load(targetFile)

print(len(features[0]))
print(target[12])
print(images[0])

#images[12].reshape(imageShape)

cv2.imshow('Image', images[12])

cv2.waitKey(0)