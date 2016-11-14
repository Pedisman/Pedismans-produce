# import necessary packages
import cv2
import numpy as np

imageFile = "./images.dat.npy"
featureFile = "./features.dat.npy"
targetFile = "./targets.dat.npy"

hog = cv2.HOGDescriptor()

# desired window size
wHeight = 1080
wWidth = 1980

#scaled image size
Ntrain = 28 # consistent with what is currently used

imageArray = []
featureArray = []
targetArray = []

filepath = 'digitTrain.png'

image = cv2.imread(filepath, 0)

cv2.imshow('input', image)
cv2.waitKey(0)

# convert the resized image to grayscale, blur it slightly,
# and threshold it
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(image, (5, 5), 0)
#thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)[1]
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, (5,5), iterations = 20)
#thresh = cv2.dilate(thresh, (20, 20), iterations = 3)
#edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

#thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

cv2.imshow("dilated", thresh)
cv2.waitKey(0)

__, contours, im2 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


for i, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)
    print(x, y, w, h)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    ROI = thresh[y:y + h , x:x + w]
    scaledROI = cv2.resize(ROI, (Ntrain,Ntrain))
    cv2.imshow('letter', ROI)
    cv2.imshow('scaled letter', scaledROI)
    character = cv2.waitKey(0)
    print(chr(character)) # shows that it works
    if character == 9: # tab is a 9
        pass #skip if human cant identify training sample
    else:
        # row in scaledROI
        imageArray.insert(-1, scaledROI)
        featureArray.insert(-1, scaledROI.flatten())
        targetArray.insert(-1, chr(character))

    if character == 27: # esc key breaks loop
        break

np.save(imageFile, np.array(imageArray))
np.save(featureFile, np.array(featureArray))
np.save(targetFile, np.array(targetArray))

#process image
imS = cv2.resize(thresh, (1920/2,1080/2))

cv2.imshow("Image", imS)

cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", 1920/2, 1080/2)

cv2.waitKey(0)
