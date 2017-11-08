import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import numpy as np
import cv2
from CTScan import CTScan
from skimage.io import imread
from skimage import data_dir
from skimage.transform import radon, rescale
from Scanner import Scanner
from Scanner2D import Scanner2D


# # load original image
# lenna = cv2.imread("SheppLogan_Phantom.png")
# lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)
# print(lenna.shape)
# print("input image")
# plt.imshow(lenna, cmap='gray')
# plt.show()
# plt.close()
#
# angleIncrement = 45
# # make CT Scan object
# CT = CTScan(lenna)
#
# currentAngle = 0
#
# # plot one pass Radon
# fig, ax1 = plt.subplots()
# values = CT.onePassRadon(currentAngle)
# ax1.set_title("1D Sinogram")
# plt.plot(values)
# fig.savefig('plot.png')
# print(values)



lenna = cv2.imread("testImage2.png")
lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)
print(lenna.shape)
# Scanner = Scanner(lenna, 1)
# Scanner.getOneSinogram(0)

Scanner2 = Scanner2D(lenna, 180)
Scanner2.radon2D()
radon_transf = Scanner2.getRadonImage()

cv2.imshow("Radon Transform", radon_transf)
cv2.waitKey()


# while currentAngle <= 90:
#     # rotate image
#     lennaRotated = CT.rotateImage(currentAngle)
#     print("rotated image")
#     plt.imshow(lennaRotated, cmap='gray')
#     plt.show()
#     plt.close()
#
#     # plot one pass Radon
#     values = CT.onePassRadon(currentAngle)
#     plt.plot(values)
#     plt.show()
#     plt.close()
#     print(values)
#
#     currentAngle += angleIncrement

# image = imread("SheppLogan_Phantom.png", as_grey=True)
# #image = rescale(image, scale=0.4, mode='reflect')
#
# #fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
# fig, ax1 = plt.subplots()
# #ax1.set_title("Original")
# #ax1.imshow(image, cmap='gray')
# print(image.shape)
#
# test = (1, 1)
#
# #theta = np.linspace(0., 180., max(image.shape), endpoint=False)
# theta = np.linspace(90., 90., max(image.shape), endpoint=False)
#
# print(theta)
# sinogram = radon(image, theta=theta, circle=True)
# ax1.set_title("Radon transform\n(Sinogram)")
# #ax2.set_xlabel("Projection angle (deg)")
# #ax2.set_ylabel("Projection position (pixels)")
# plt.plot(sinogram)
# #ax2.imshow(sinogram, cmap='gray',
# #           extent=(0, 180, 0, sinogram.shape[0]), aspect='auto')
# plt.show()
# plt.close()
#
# fig.tight_layout()