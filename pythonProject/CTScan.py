import cv2

class CTScan:

    inputImage = None  # cv2 image

    def __init__(self, image):
        self.inputImage = image

    def onePassRadon(self, angleAmount):
        """ Do one pass of radon , return list of 1D values """
        rotated_image = self.rotateImage(angleAmount)
        (N, M) = rotated_image.shape
        radon_values = [0]*N
        for radon_line in range(N):
            linesum = 0
            for pixel in range(M):
                linesum += rotated_image[radon_line][pixel]
            radon_values[radon_line] = linesum
        return radon_values

    def rotateImage(self, angleAmount):
        (N, M) = self.inputImage.shape
        RotM = cv2.getRotationMatrix2D((N / 2, M / 2), angleAmount, 1)
        rotated_image = cv2.warpAffine(self.inputImage, RotM, (N, M))
        return rotated_image