import cv2

filename = 'digit7.PNG'
image = cv2.imread(filename, 0)

cv2.imshow('yo', image)
cv2.waitKey(0)
