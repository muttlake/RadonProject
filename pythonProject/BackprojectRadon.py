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

        rotated_backProjection = self.rotateMatrix(self.backProjectionMatrix, angle * -1)
        (N, M) = rotated_backProjection.shape
        print("rotated_backProjection.shape: ", rotated_backProjection.shape)
        for row in range(N):
            for col in range(len(radonLineValues)):
                colShift = round(M / 4)
                currentValue = rotated_backProjection[row][col + colShift]
                backprojectionValue = self.radonMatrix[col, angleIndex]
                rotated_backProjection[row][col + colShift] = currentValue + backprojectionValue

        self.backProjectionMatrix = self.rotateMatrix(rotated_backProjection, angle)
        return self.backProjectionMatrix


    def rotateMatrix(self, inputMatrix, angleAmount):
        (N, M) = inputMatrix.shape
        RotM = cv2.getRotationMatrix2D((N / 2, M / 2), angleAmount, 1)
        rotated_matrix = cv2.warpAffine(inputMatrix, RotM, (N, M))
        return rotated_matrix
