import matplotlib.pyplot as plt
import numpy as np
import cv2

#img = cv2.imread()

#contours, im2 = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



foods = ['grape', 'cherry', 'mango']
featureFile = "./features.dat.npy"
targetFile = "./targets.dat.npy"

totalArray = []

joe = np.zeros((10,10))
hanna = 255*np.ones((10,10))
print(joe)

replacement = []
for line in joe:
    print(line)
    replacement.extend(line)

replacement2 = []

'''
for line in hanna:
    print(line)
    replacement2.extend(line)
'''
joe = joe.flatten()
hanna =hanna.flatten()

print(replacement)
print(len(replacement))

totalArray = []

totalArray.insert(-1, joe)
totalArray.insert(-1, hanna)

print(np.array(totalArray))
'''
hanna = 255*np.ones((10,10))

totalArray.insert(-1, joe)
totalArray.insert(-1, hanna)

print(totalArray)

np.save(featureFile, np.array(totalArray))
np.save(targetFile, np.array(joe))

z = np.load(featureFile)#.tolist()
#z = np.load(targetFile)#.tolist()
print("z is: " + str(z))

cv2.imshow('image', z[0])
test = cv2.waitKey(0)

print(test)
print(chr(test))

#plt.imshow(Wz, cmap=plt.cm.gray_r, interpolation="nearest")
#plt.show()
'''