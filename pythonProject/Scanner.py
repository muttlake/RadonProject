import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from CTScan import CTScan


class Scanner:

    inputImage = None

    def __init__(self, image):
        self.inputImage = image

    def getOneSinogram(self, angle):
        """ Get a single sinogram for CT """
        CT = CTScan(self.inputImage)
        # plot one pass Radon
        fig, ax1 = plt.subplots()
        values = CT.onePassRadon(angle)
        titleString = "1D Sinogram at Angle: " + str(angle) + "°"
        ax1.set_title(titleString)
        plt.plot(values)
        fig.savefig('scanner_plot.png')