# import necessary packages
import cv2
import numpy as np

imageFile = "./images.dat.npy"
featureFile = "./features.dat.npy"
targetFile = "./targets.dat.npy"

# desired window size
wHeight = 1080
wWidth = 1980

#scaled image size
Ntrain = 28 # consistent with what is currently used

imageArray = []
featureArray = []
targetArray = []

filepath = 'scoresheetExample.jpg'

image = cv2.imread(filepath)


def isSquare(c):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    if len(approx == 4):
        return True
    else:
        return False


# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

# get dimensions of the image
height, width, channels = image.shape

# Hough parameters
maxLineGap = 100
minLineLength = 200

centreDivider = height/2

print(minLineLength)

lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)

topHeight = height
botHeight = 0

#previous vertical divider
xPrev = None
overWriteWidth = 81

for line in lines:
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[0][2]
    y2 = line[0][3]
    lineLength = np.sqrt((x1-x2)**2 + (y1-y2)**2)
    print(lineLength)
    Angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi
    Angle = abs(Angle)
    if (lineLength >= (height // 4) and (Angle == 90 or Angle == 270)):
        if (xPrev != None):
            overWriteAfter = (x1-xPrev)//2 + xPrev
            cv2.line(thresh, (overWriteAfter, 0), (overWriteAfter, height), (255, 255, 255), overWriteWidth)
            overWriteBefore = xPrev - (x1-xPrev)//2
            cv2.line(thresh, (overWriteBefore, 0), (overWriteBefore, height), (255, 255, 255), overWriteWidth)
            overWriteAfter2 = (x1-xPrev)//2 + x1
            cv2.line(thresh, (overWriteAfter2, 0), (overWriteAfter2, height), (255, 255, 255), overWriteWidth)
        cv2.line(thresh, (x1, 0), (x2, height), (255, 255, 255), 20)
        xPrev = x1
    if (lineLength >= minLineLength and (Angle == 0 or Angle == 180)):
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 1)
        if (y1 > centreDivider and y1 < topHeight):
            topHeight = y1
        elif (y1 < centreDivider and y1 > botHeight):
            botHeight = y1


print(topHeight)
print(botHeight)

#horizontal divider lines
lineThickness = 1
cv2.line(image, (0, topHeight), (width, topHeight), (0, 0, 255), lineThickness)
cv2.line(image, (0, botHeight), (width, botHeight), (0, 0, 255), lineThickness)

#obtain a new region of interest after removing the top and bottom blocks of the scoresheet
img2 = thresh[botHeight + lineThickness:topHeight - lineThickness, 0:width] #[Y1:Y2, X1:X2]

thresh = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

__, contours, im2 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


for i, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)
    print(x, y, w, h)
    cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
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
imS = cv2.resize(img2, (1920/2,1080/2))

cv2.imshow("Image", imS)

cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", 1920/2, 1080/2)

cv2.waitKey(0)
