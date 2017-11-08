from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import *
import cv2
import numpy as np
import time
from Scanner import Scanner
from Scanner2D import Scanner2D

class ProjectUI:


    inputImage = None    # cv2 image
    numAngles = None
    ctAcquisitionImage = None  # cv2 image
    currentAngleIndex = None

    inputImageLabel = None
    statusLabel = None
    ctAcquisitionImageLabel = None
    ctScan1DLabel = None

    numAnglesTextBox = None
    angleIncrementLabel = None

    def __init__(self, master): # master means root or main window

        ## ****** Main Menu ******
        menu = Menu(master)

        master.config(menu=menu)
        subMenu = Menu(menu)

        menu.add_cascade(label="File", menu=subMenu)
        subMenu.add_command(label="Exit", command=quit)

        ## ****** Toolbar ******
        toolbar = Frame(master, bg="azure3")

        insertButton = Button(toolbar, text="Get Image", command=self.getInputImage)
        insertButton.pack(side=LEFT, padx=20, pady=20)

        quitButton = Button(toolbar, text="Quit", command=quit)
        quitButton.pack(side=RIGHT, padx=20, pady=20)

        ctScanButton = Button(toolbar, text="CT Scan 2D", command=self.getCTScan)
        ctScanButton.pack(side=RIGHT, padx=20, pady=20)

        ctStepwiseScanButton = Button(toolbar, text="CT Scan Step", command=self.doStepwiseCTScan)
        ctStepwiseScanButton.pack(side=RIGHT, padx=20, pady=20)

        #ctScan1DButton = Button(toolbar, text="CT Scan 1D", command=self.getFirstAngleDCTScan)
        #ctScan1DButton.pack(side=RIGHT, padx=20, pady=20)

        toolbar.pack(side=TOP, fill=X)

        ## ****** Status Bar ******
        self.statusLabel = Label(root, text="Started Project GUI", bd=1, relief=SUNKEN, anchor=W)  # bd = border, anchor = West
        self.statusLabel.pack(side=BOTTOM, fill=X)

        ## ****** Main Window Frame ******
        mainFrame = Frame(root, width=1500, height=1000, bg="gainsboro")  # frame is a blank widget
        mainFrame.pack()

        ## ****** Input image ******
        empty_image = cv2.imread("empty_image.jpg")
        empty_image_display = self.makeDisplayImage(empty_image, (400, 400))
        self.inputImageLabel = Label(mainFrame, width=400, height=400, image=empty_image_display)
        self.inputImageLabel.place(x=50, y=25)

        degree0Label = Label(mainFrame, text="0°")
        degree0Label.place(x=240, y=5)

        degree90Label = Label(mainFrame, text="90°")
        degree90Label.place(x=455, y=225)

        degree180Label = Label(mainFrame, text="180°")
        degree180Label.place(x=225, y=427)

        ## ****** Make Arrow above 1D Radon Transform ******

        canvas = Canvas(mainFrame, width=500, height=30, bg="gainsboro", bd=0, highlightthickness=0, relief='ridge')
        canvas.place(x=500, y=30)
        blackLine = canvas.create_line(0, 15, 500, 15, tags=("line",), arrow="last", fill="black")
        radonLabel = Label(mainFrame, text = "CT Scan (Radon Transform)", bg="gainsboro", font=("Helvetica", 16))
        radonLabel.place(x=650, y=20)

        ## ****** 1D CT Scan ******
        self.ctScan1DLabel = Label(mainFrame, width=400, height=300, image=empty_image_display)
        self.ctScan1DLabel.place(x=550, y=75)

        ## ****** CT Scan Image ******
        self.ctAcquisitionImageLabel = Label(mainFrame, width=400, height=400, image=empty_image_display)
        self.ctAcquisitionImageLabel.place(x=1050, y=25)

        ## ****** Get Number of Angles between 0 and 180 ******
        numAnglesLabel = Label(mainFrame, text="Enter number of angles desired (will range from 0° to 180°):")
        numAnglesLabel.place(x = 30, y=450)
        self.numAnglesTextBox = Text(mainFrame, height=1, width=5, bg="light gray")
        self.numAnglesTextBox.place(x=425, y=450)
        buttonCommitNumAngles = Button(mainFrame, height=1, width=10, text="Commit",
                                       command=self.retrieve_num_angles_input)
        buttonCommitNumAngles.place(x=400, y=475)
        self.angleIncrementLabel = Label(mainFrame, text="", bg="gainsboro", fg="red")
        self.angleIncrementLabel.place(x=30, y=475)


    def setStatus(self, statusString):
        self.statusLabel.configure(text=statusString)
        self.statusLabel.text = statusString

    def getInputImage(self):
        filename = filedialog.askopenfilename()
        print("Setting input image to: ", filename)

        self.inputImage = cv2.imread(filename)
        self.inputImage = cv2.cvtColor(self.inputImage, cv2.COLOR_RGB2GRAY)

        displayImage = self.makeDisplayImage(self.inputImage, (400, 400))

        self.inputImageLabel.configure(image=displayImage)
        self.inputImageLabel.image = displayImage
        self.setStatus("Loaded input image.")

    def makeDisplayImage(self, cv2_image, shape):
        disp_im = Image.fromarray(cv2_image)
        disp_im = disp_im.resize(shape, Image.ANTIALIAS)
        return ImageTk.PhotoImage(disp_im)

    def getCTScan(self):
        """ Get CT scan using CTScan class"""
        if self.inputImage is not None:
            numAngle2 = 180
            if self.numAngles is not None:
                numAngle2 = int(self.numAngles)

            Scanner2 = Scanner2D(self.inputImage, numAngle2)
            Scanner2.radon2D()
            radon_transf = Scanner2.getRadonImage()
            print(radon_transf.shape)

            displayImage = self.makeDisplayImage(radon_transf, (400, 400))

            self.ctAcquisitionImageLabel.configure(image=displayImage)
            self.ctAcquisitionImageLabel.image = displayImage
            self.setStatus("Ran Full CT Scan")
        else:
            print("No input image to do 1D transform.")
            print("No input image to transform.")

    def doStepwiseCTScan(self):
        """Step through each angle and do CT scan, display 1D and 2D stepwise results"""
        numAngle2 = 10
        if self.numAngles is not None:
            numAngle2 = int(self.numAngles)

        Scanner2Dobject = Scanner2D(self.inputImage, numAngle2)
        anglesArray = Scanner2Dobject.getAnglesArray()

        if self.currentAngleIndex is None:
            self.currentAngleIndex = 0
            angle = 0
        else:
            self.currentAngleIndex += 1
            self.currentAngleIndex = self.currentAngleIndex % len(anglesArray)
            angle = anglesArray[self.currentAngleIndex]

        self.do1DCTScan(angle)


    def retrieve_num_angles_input(self):
        self.numAngles = self.numAnglesTextBox.get("1.0", "end-1c")
        outputString = ""
        if self.numAngles == "":
            outputString = "No number entered for number of angles."
            self.numAngles="1"
        else:
            angleIncrement = np.float(180)/np.float(self.numAngles)
            outputString = "The angle increment will be " + str(angleIncrement) + "°"
        self.angleIncrementLabel.config(text=outputString)
        self.angleIncrementLabel.text = outputString
        #print(self.numAngles)

    def doNothing(self):
        print("Not implemented yet.")

    def do1DCTScan(self, angle):
        """ Get 1D CT scan using CTScan class"""
        Scanner1 = Scanner(self.inputImage)
        Scanner1.getOneSinogram(angle)

        sinogram1DImage= cv2.imread("scanner_plot.png")
        sinogram1DImage = cv2.cvtColor(sinogram1DImage, cv2.COLOR_RGB2GRAY)
        displayImage = self.makeDisplayImage(sinogram1DImage, (400, 300))

        self.ctScan1DLabel.configure(image=displayImage)
        self.ctScan1DLabel.image = displayImage
        statusString = "Ran 1D CT Scan at angle  " + str(angle) + "°"
        self.setStatus(statusString)





# start Project GUI
root = Tk()

p = ProjectUI(root)

root.mainloop()

