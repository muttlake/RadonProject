import cv2
import numpy as np

class BackprojectRadon:

    def __init__(self, inputIm, angArray, radonMat, backProjM):
        self.inputImage = inputIm
        self.anglesArray = angArray
        self.radonMatrix = radonMat

        (N, M) = self.inputImage.shape
        self.backProjectionMatrix = backProjM
        self.outputImage = np.zeros((N, M), np.uint8)

    def stepwiseBackprojection(self, angleIndex):
        """ Do one pass of radon , return list of 1D values """
        angle = self.anglesArray[angleIndex]

        (NR, AR) = self.radonMatrix.shape
        radonLineValues = [0] * NR

        rotated_backProjection = self.rotateMatrix(self.backProjectionMatrix, angle)
        (N, M) = rotated_backProjection.shape
        print("rotated_backProjection.shape: ", rotated_backProjection.shape)
        for row in range(N):
            for col in range(len(radonLineValues)):
                colShift = round(M / 4)
                currentValue = rotated_backProjection[row][col + colShift]
                backprojectionValue = self.radonMatrix[col, angleIndex]
                rotated_backProjection[row][(M-1) - (col + colShift)] = currentValue + backprojectionValue

        self.backProjectionMatrix = self.rotateMatrix(rotated_backProjection, angle*-1)
        return self.backProjectionMatrix


    def rotateMatrix(self, inputMatrix, angleAmount):
        (N, M) = inputMatrix.shape
        RotM = cv2.getRotationMatrix2D((N / 2, M / 2), angleAmount, 1)
        rotated_matrix = cv2.warpAffine(inputMatrix, RotM, (N, M))
        return rotated_matrix

    # Getting Backprojection image

    def getBackprojectionImage(self):
        """ return uint8 radon image"""
        maxValue = self.getMaxValue()
        if(maxValue == 0):
            maxValue = 1
        (N, M) = self.inputImage.shape
        (P, Q) = self.backProjectionMatrix.shape

        row_shift = round((P / 4))
        col_shift = round((Q / 4))

        for row in range(N):
            for col in range(M):
                image_value = self.backProjectionMatrix[row + row_shift][col + col_shift]/maxValue * 255
                self.outputImage[row][col] = np.round(image_value)
        #self.outputImage = self.post_process_image(self.outputImage)
        return self.outputImage

    def getPostProcessedBackprojectionImage(self, image):
        """ return uint8 radon image"""
        post_processed_image = self.post_process_image(image)
        return post_processed_image

    def getMaxValue(self):
        maxValue = -1
        #(N, M) = self.inputImage.shape
        (P, Q) = self.backProjectionMatrix.shape
        for row in range(P):
            for col in range(Q):
                if self.backProjectionMatrix[row][col] > maxValue:
                    maxValue = self.backProjectionMatrix[row][col]
        return maxValue

    def cleanBackprojectionMatrix(self):
        """set all values to zero"""
        (N, M) = self.inputImage.shape
        self.backProjectionMatrix = np.zeros((N, M), np.float32)

    def getMaxImageValue(self, image):
        maxValue = -1
        (P, Q) = image.shape
        for row in range(P):
            for col in range(Q):
                if image[row][col] > maxValue:
                    maxValue = image[row][col]
        return maxValue

    def getMinImageValue(self, image):
        minValue = -1
        (P, Q) = image.shape
        for row in range(P):
            for col in range(Q):
                if image[row][col] < minValue or minValue == -1:
                    minValue = image[row][col]
        return minValue

    def post_process_image(self, image):
        """Do contrast stretch on the image"""
        # get min, max values, then do stretch
        image_hist = self.compute_histogram(image)

        A = self.findMinHistValue(image_hist)
        B = self.findMaxHistValue(image_hist)

        if B - A == 0:
            A = 0
            B = 255
        P = 255/(B - A) # P = ((K-1)/(B-A)), K = 255

        # Now do full contrast stretch formula : P = ((K-1)/(B-A))
        (N, M) = image.shape
        image_full_contrast_stretch = np.zeros((N, M), np.uint8)
        for ii in range(N):
            for jj in range(M):
                image_full_contrast_stretch[ii, jj] = P * (image[ii][jj] - A)
        return image_full_contrast_stretch

    def compute_histogram(self, image):
        """Computes the histogram of the input image takes as input: image: a grey scale image returns a histogram"""
        hist = [0] * 256
        (rows, columns) = image.shape
        for row in range(rows):
            for column in range(columns):
                intensity = image[row][column]
                hist[intensity] = hist[intensity] + 1
        return hist

    def findMinHistValue(self, hist):
        """Get minimum nonempty histogram value for image."""
        minValue = -1
        i = 0
        foundNonEmptyValue = False
        while i < len(hist) and not foundNonEmptyValue:
            if hist[i] > 0:
                minValue = i
                foundNonEmptyValue = True
            i = i + 1
        return minValue

    def findMaxHistValue(self, hist):
        """Get minimum nonempty histogram value for image."""
        maxValue = -1
        i = len(hist) - 1
        foundNonEmptyValue = False
        while i >= 0 and not foundNonEmptyValue:
            if hist[i] > 0:
                maxValue = i
                foundNonEmptyValue = True
            i = i - 1
        return maxValue