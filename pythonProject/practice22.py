import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import numpy as np
import cv2
from CTScan import CTScan

# load original image
lenna = cv2.imread("Lenna.png")
lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)
print(lenna.shape)
print("input image")
plt.imshow(lenna, cmap='gray')
plt.show()
plt.close()

angleIncrement = 45
# make CT Scan object
CT = CTScan(lenna)

currentAngle = 0

while currentAngle <= 90:
    # rotate image
    lennaRotated = CT.rotateImage(currentAngle)
    print("rotated image")
    plt.imshow(lennaRotated, cmap='gray')
    plt.show()
    plt.close()

    # plot one pass Radon
    values = CT.onePassRadon(currentAngle)
    plt.plot(values)
    plt.show()
    plt.close()
    print(values)

    currentAngle += angleIncrement

