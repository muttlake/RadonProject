import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from skimage.transform import radon

class Scanner2DSKI:

    numAngles = None  # number of Radon Scans
    inputImage = None
    radonOutput = None
    anglesArray = []
    fig = None
    ax1 = None


    def __init__(self, image, numAngles):
        """ Make angles array and initialize radon output matrix"""
        self.inputImage = image

        self.numAngles = numAngles
        self.convertPassesToAngleArray()

        (N, M) = self.inputImage.shape
        self.radonOutput = np.zeros((N, self.numAngles), np.float32)

        self.fig, self.ax1 = plt.subplots()


    def radon2D(self):
        """ Do one pass of radon , return list of 1D values """
        (N, M) = self.inputImage.shape
        self.cleanRadonMatrix()

        angleIndex = 0
        for angle in self.anglesArray:
            theta = np.linspace(angle, angle, 1, endpoint=False)
            sinogram = radon(self.inputImage, theta=theta, circle=True)
            for pixel in range(N):
                self.radonOutput[pixel][angleIndex] = sinogram[pixel]
            angleIndex += 1


    def cleanRadonMatrix(self):
        """clean radon matrix"""
        (N, M) = self.inputImage.shape
        self.radonOutput = np.zeros((N, self.numAngles), np.float32)


    def stepwiseRadon2D(self, angle):
        """ Do one pass of radon , return list of 1D values """
        theta = np.linspace(angle, angle, 1, endpoint=False)
        sinogram = radon(self.inputImage, theta=theta, circle=True)

        for pixel in range(N):
            self.radonOutput[pixel][int(angle)] = sinogram[pixel]


    def convertPassesToAngleArray(self):
        """output the angle increment as a float over 180°"""
        self.anglesArray = []
        if self.numAngles <= 0:
            self.numAngles = 1
        if self.numAngles > 181:
            self.numAngles = 181
        self.anglesArray = np.linspace(0, 180, self.numAngles, endpoint=True)


    def getAnglesArray(self):
        """return angles array"""
        return self.anglesArray


    def saveRadon2DImage(self):
        """ Save radon 2D image to file"""
        self.ax1.set_title("Radon transform\n(Sinogram)")
        self.ax1.set_xlabel("Projection angle (deg)")
        self.ax1.set_ylabel("Projection position (pixels)")
        self.ax1.imshow(self.radonOutput, cmap=plt.cm.Greys_r, extent=(0, 180, 0, self.radonOutput.shape[0]), aspect='auto')
        self.fig.savefig('radon2D_Image.png')
        self.ax1.cla()