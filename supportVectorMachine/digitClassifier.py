import matplotlib.pyplot as plt
import numpy as np
import cv2

from sklearn import datasets
from sklearn import svm
from sklearn import neural_network
from sklearn import neighbors

MLPClassifier = neural_network.MLPClassifier

KNeighborsClassifier = neighbors.KNeighborsClassifier

imageFile = "./images.dat.npy"
featureFile = "./features.dat.npy"
targetFile = "./targets.dat.npy"

features = np.load(featureFile)
images = np.load(imageFile)
target = np.load(targetFile)

digits = datasets.load_digits()
#clf = svm.SVC(gamma=0.00001) #, C=100) C is the error term
clf = KNeighborsClassifier(n_neighbors = 7)
#clf = svm.LinearSVC()
#clf = MLPClassifier()

filename = "digit7.png"

testImage = cv2.imread(filename, 0)

print(testImage)

cv2.imshow("test Image", testImage)
cv2.waitKey(0)

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
    scaledROI = cv2.resize(ROI, Nshape)

    cv2.imshow("scaledROI", scaledROI)
    cv2.waitKey(0)

    return scaledROI.flatten()

testOut = process(testImage)

print(len(digits.data))

print(digits.data[0])# 8x8 = 64 features
print(digits.data[0].shape)
print(digits.images[0])

print(digits.target[0])# what the numbers meant to be

output = []

#hog classification vector
#cv2.hog.compute(digits.images[0], output, Size(8,8), )

halfway = len(digits.data//2)

print(halfway)

#x, y = digits.data[:halfway], digits.target[:halfway]

x, y = features, target
clf.fit(x, y)

gobi = np.zeros((8,8))
print(gobi)

print(digits.images[0][0])
print(len(digits.images[0]))

#for i in

#hogImg = hog(digits.images[0])

#print(hogImg)

def test(unknown, target): #e.g. digits.data, digits.target
    count = 0
    for i, dat in enumerate(unknown):
        dat = dat.reshape(1,-1)
        if (clf.predict(dat)[0] == target[i]):
            count += 1
            print(count, clf.predict(dat)[0], target[i])
            #print(digits.target[i])
            #print(count)
    return 100*len(unknown)/count

#print(clf.predict(digits.data[-6])[0])

index = 120

#print(clf.predict(features[index].reshape(1, -1)))
print(clf.predict(testOut.reshape(1, -1)))

#cv2.imshow("Image", images[index])

cv2.imshow("Image", testImage)

cv2.waitKey(0)

'''
print('Prediction:', clf.predict(digits.data[-6]))
plt.imshow(digits.images[-6], cmap=plt.cm.gray_r, interpolation="nearest")
plt.show()
'''
