import cv2
import numpy as np
from CTScan import CTScan
from skimage.io import imread
from skimage import data_dir
from skimage.transform import radon, rescale

class Scanner2D:

    numPasses = None  # number of Radon Scans
    inputImage = None
    radonOutput = None
    radonImage = None
    anglesArray = []
    startOverStepWise = None

    def __init__(self, image, passes):
        self.inputImage = image
        self.numPasses = passes
        (N, M) = self.inputImage.shape
        self.convertPassesToAngleArray()
        numAngles = len(self.anglesArray)
        #print("This is the angles array")
        #print(self.anglesArray)
        self.radonOutput = np.zeros((N, numAngles), np.float32)
        self.radonImage = np.zeros((N, numAngles), np.uint8)
        self.angleIndex = False

    def radon2D(self):
        """ Do one pass of radon , return list of 1D values """
        (N, M) = self.inputImage.shape
        angleCount = len(self.anglesArray)
        self.cleanRadonMatrix()

        CT = CTScan(self.inputImage)
        angleIndex = 0

        for angle in self.anglesArray:
            values = CT.onePassRadon(angle)
            #print("\nAngle = ", angle)
            #print(values)
            valueIndex = 0
            valueCount = len(values)
            for value in values:
                self.radonOutput[valueIndex][angleCount - angleIndex - 1] = values[valueIndex]
                valueIndex += 1
            #print("\nNow radon matrix is : ")
            #self.printUnsignedImage(self.radonOutput)
            angleIndex += 1

    def cleanRadonMatrix(self):
        """clean radon matrix"""
        (N, M) = self.inputImage.shape
        angleCount = len(self.anglesArray)
        self.radonOutput = np.zeros((N, angleCount), np.float32)


    def stepwiseRadon2D(self, angleIndex):
        """ Do one pass of radon , return list of 1D values """
        if angleIndex == 0 or self.startOverStepWise:
            self.cleanRadonMatrix()
            angleIndex = 0
        CT = CTScan(self.inputImage)
        angleCount = len(self.anglesArray)
        angle = self.anglesArray[angleIndex]
        values = CT.onePassRadon(angle)
        valueIndex = 0
        valueCount = len(values)
        for value in values:
            self.radonOutput[valueIndex][angleCount - angleIndex - 1] = values[valueIndex]
            valueIndex += 1

    def convertPassesToAngleArray(self):
        """output the angle increment as a float over 180°"""
        self.anglesArray = []
        if self.numPasses <= 0:
            #print("setting numPasses to 1")
            self.numPasses = 1

        if self.numPasses == 1:
            self.anglesArray.append(0.00)
        else:
            angleIncrement = np.float(180)/np.float(self.numPasses)
            currentAngle = 0.00
            while currentAngle <= 180:
                self.anglesArray.append(currentAngle)
                currentAngle += angleIncrement

    def getAnglesArray(self):
        """return angles array"""
        return self.anglesArray


    def getRadonImage(self):
        """ return uint8 radon image"""
        maxValue = self.getMaxRadonValue()
        (N, M) = self.radonOutput.shape
        for row in range(N):
            for col in range(M):
                image_value = self.radonOutput[row][col]/maxValue * 255
                self.radonImage[row][col] = np.round(image_value)
        return self.radonImage


    def getRawRadonMatrix(self):
        """ return radon matrix"""
        return self.radonOutput

    def getRadonAnglesArray(self):
        """ return radon angles """
        return self.anglesArray

    def getMaxRadonValue(self):
        maxValue = -1
        (N, M) = self.radonOutput.shape
        for row in range(N):
            for col in range(M):
                if self.radonOutput[row][col] > maxValue:
                    maxValue = self.radonOutput[row][col]
        return maxValue

    def printUnsignedImage(self, image):
        (N, M) = image.shape
        if N < 20:
            for i in range(N):
                for j in range(M):
                    print('{: <8}'.format(image[i][j]), "  ", end=""),
                print("", end="\n"),
        else:
            print("Image too large to print.")