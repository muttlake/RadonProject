from matplotlib import pyplot as plt
import numpy as np
import cv2


class CTScan:

    image = None  # cv2 image
    angleIncrement = None

    def __init__(self, image, angleIncrement):
        self.image = image
        self.angleIncrement = angleIncrement

    def doRadon(self, image):
        """ Loop through angle increments, rotate image, do radon passes"""
        (N, M) = image.shape
        num_radon_passes = np.int(np.round(np.floor(180/self.angleIncrement)))
        radon_transform = np.zeros((N, num_radon_passes), np.float32)
        currentAngle = 0
        currentRadonPass = 0
        while currentAngle < 180:
            print("Currently working on angle: ", currentAngle)
            RotM = cv2.getRotationMatrix2D((N/2, M/2), currentAngle, 1)
            rotated_image = cv2.warpAffine(image, RotM, (N, M))
            new_radon_values = self.onePassRadon(rotated_image)
            # cv2.imshow("Rotated Image", rotated_image)
            # cv2.waitKey()
            # plt.plot(new_radon_values)
            # plt.show()
            radon_transform = self.addCurrentRadonValues(radon_transform, new_radon_values, currentRadonPass)
            currentAngle += self.angleIncrement
            currentRadonPass += 1

        return radon_transform

    def onePassRadon(self, image):
        """ Do one pass of radon , return list of 1D values """
        (N, M) = image.shape
        radon_values = [0]*N
        for radon_line in range(N):
            linesum = 0
            for pixel in range(M):
                linesum += image[radon_line][pixel]
            radon_values[radon_line] = linesum
        return radon_values

    def addCurrentRadonValues(self, radon_transform, currentValues, currentPass):
        """ Add current radon values"""
        (N, num_passes) = radon_transform.shape
        radon_transform_out = np.zeros((N, num_passes), np.float32)
        for pixel in range(N):
            radon_transform_out[pixel][currentPass] = currentValues[pixel]
        return radon_transform_out