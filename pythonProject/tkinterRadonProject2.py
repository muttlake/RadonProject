from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import *
import cv2
import numpy as np
import time
from Scanner import Scanner
from Scanner2D import Scanner2D
from Scanner2DSKI import Scanner2DSKI

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

    StepWiseScanner2D = None
    changeOccurred = False

    mainframe = None

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

        ctScanSKIButton = Button(toolbar, text="CT Scan Scikit Full", command=self.getCTScanSKI)
        ctScanSKIButton.pack(side=RIGHT, padx=20, pady=20)

        ctScanButton = Button(toolbar, text="CT Scan Full", command=self.getCTScan)
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
        self.mainframe = Frame(root, width=1500, height=1000, bg="gainsboro")  # frame is a blank widget
        self.mainframe.pack()

        ## ****** Input image ******
        empty_image = cv2.imread("empty_image.jpg")
        empty_image_display = self.makeDisplayImage(empty_image, (400, 400))
        self.inputImageLabel = Label(self.mainframe, width=400, height=400, image=empty_image_display)
        self.inputImageLabel.place(x=50, y=25)

        degree180Label = Label(self.mainframe, text="180°", bg="gainsboro")
        degree180Label.place(x=240, y=2)

        # degree90Label = Label(self.mainframe, text="90°")
        # degree90Label.place(x=455, y=225)

        degree0Label = Label(self.mainframe, text="0°", bg="gainsboro")
        degree0Label.place(x=225, y=430)


        ## ****** Make Arrow above 1D Radon Transform ******
        self.makeLeftSideArrows(0)
        self.makeRightSideArrows(0)

        ## ****** Make Arrow above 1D Radon Transform ******
        canvas = Canvas(self.mainframe, width=280, height=30, bg="gainsboro", bd=0, highlightthickness=0, relief='ridge')
        canvas.place(x=520, y=30)
        blackLine = canvas.create_line(0, 15, 280, 15, tags=("line",), arrow="last", fill="black")
        radonLabel = Label(self.mainframe, text = "CT Scan (Radon Transform)", bg="gainsboro", font=("Helvetica", 16))
        radonLabel.place(x=560, y=20)

        ## ****** 1D CT Scan ******
        self.ctScan1DLabel = Label(self.mainframe, width=300, height=225, image=empty_image_display)
        self.ctScan1DLabel.place(x=510, y=75)

        ## ****** CT Scan Image ******
        self.ctAcquisitionImageLabel = Label(self.mainframe, width=640, height=480, image=empty_image_display)
        self.ctAcquisitionImageLabel.place(x=835, y=5)

        ## ****** Get Number of Angles between 0 and 180 ******
        numAnglesLabel = Label(self.mainframe, text="Enter number of angles desired (will range from 0° to 180°):")
        numAnglesLabel.place(x = 30, y=500)
        self.numAnglesTextBox = Text(self.mainframe, height=1, width=5, bg="light gray")
        self.numAnglesTextBox.place(x=425, y=500)
        buttonCommitNumAngles = Button(self.mainframe, height=1, width=10, text="Commit",
                                       command=self.retrieve_num_angles_input)
        buttonCommitNumAngles.place(x=400, y=525)
        self.angleIncrementLabel = Label(self.mainframe, text="", bg="gainsboro", fg="red")
        self.angleIncrementLabel.place(x=30, y=525)


    def setStatus(self, statusString):
        self.statusLabel.configure(text=statusString)
        self.statusLabel.text = statusString

    def getInputImage(self):
        filename = filedialog.askopenfilename()
        print("Setting input image to: ", filename)
        self.changeOccurred = True

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
            numAngle2 = 181
            if self.numAngles is not None:
                numAngle2 = int(self.numAngles)

            Scanner2 = Scanner2D(self.inputImage, numAngle2)
            Scanner2.radon2D()
            radon_transf = Scanner2.getRadonImage()
            print(radon_transf.shape)

            displayImage = self.makeDisplayImage(radon_transf, (640, 480))

            self.makeLeftSideArrows(180)
            self.makeRightSideArrows(180)

            self.ctAcquisitionImageLabel.configure(image=displayImage)
            self.ctAcquisitionImageLabel.image = displayImage
            self.setStatus("Ran Full CT Scan")
        else:
            print("No input image to do 1D transform.")
            print("No input image to transform.")

    def getCTScanSKI(self):
        """ Get CT scan using CTScan class"""
        if self.inputImage is not None:
            numAngles2 = 181
            if self.numAngles is not None:
                numAngles2 = int(self.numAngles)


            #rint("Number of angles in getCTScanSKI: ", numAngles2)
            Scanner2 = Scanner2DSKI(self.inputImage, numAngles2)
            Scanner2.radon2D()
            Scanner2.saveRadon2DImage()

            radon_transf = cv2.imread("radon2D_Image.png")
            radon_transf = cv2.cvtColor(radon_transf, cv2.COLOR_RGB2GRAY)
            #print("Scanner2DSKI radon_transf shape: ", radon_transf.shape)
            displayImage = self.makeDisplayImage(radon_transf, (640, 480))

            self.makeLeftSideArrows(180)
            self.makeRightSideArrows(180)

            self.ctAcquisitionImageLabel.configure(image=displayImage)
            self.ctAcquisitionImageLabel.image = displayImage
            self.setStatus("Ran CT Scan for all Angles")
        else:
            print("No input image to do 1D transform.")
            print("No input image to transform.")


    def doStepwiseCTScan(self):
        """Step through each angle and do CT scan, display 1D and 2D stepwise results"""
        numAngle2 = 10
        if self.numAngles is not None:
            numAngle2 = int(self.numAngles)
        else:
            angleIncrement = np.float(180) / np.float(numAngle2)
            outputString = "Setting the angle increment to  " + str(angleIncrement) + "°"
            self.angleIncrementLabel.config(text=outputString)
            self.angleIncrementLabel.text = outputString

        if self.StepWiseScanner2D is None or self.changeOccurred:
            self.StepWiseScanner2D = Scanner2D(self.inputImage, numAngle2)
            self.StepWiseScanner2D.startOverStepWise = True
            self.currentAngleIndex = 0
            self.changeOccurred = False
            self.makeLeftSideArrows(0)
            self.makeRightSideArrows(0)

        anglesArray = self.StepWiseScanner2D.getAnglesArray()

        angle = anglesArray[self.currentAngleIndex]

        #Do 1D CT Scan
        self.do1DCTScan(angle)

        #Rotate Arrows
        self.makeLeftSideArrows(angle)
        self.makeRightSideArrows(angle)

        #Scanner2 = Scanner2D(self.inputImage, numAngle2)
        self.StepWiseScanner2D.stepwiseRadon2D(self.currentAngleIndex)
        self.StepWiseScanner2D.startOverStepWise = False
        self.currentAngleIndex += 1
        self.currentAngleIndex = self.currentAngleIndex % len(anglesArray)
        current_radon_transf = self.StepWiseScanner2D.getRadonImage()
        #print(current_radon_transf.shape)

        displayImage = self.makeDisplayImage(current_radon_transf, (640, 480))

        self.ctAcquisitionImageLabel.configure(image=displayImage)
        self.ctAcquisitionImageLabel.image = displayImage
        #self.setStatus("R")


    def retrieve_num_angles_input(self):
        self.numAngles = self.numAnglesTextBox.get("1.0", "end-1c")
        outputString = ""
        if self.numAngles == "":
            outputString = "Setting default angle increment: 18°"
            self.numAngles="10"
        else:
            angleIncrement = np.float(180)/np.float(self.numAngles)
            outputString = "The angle increment will be " + str(angleIncrement) + "°"
            self.changeOccurred = True
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
        displayImage = self.makeDisplayImage(sinogram1DImage, (300, 225))

        self.ctScan1DLabel.configure(image=displayImage)
        self.ctScan1DLabel.image = displayImage
        statusString = "Ran 1D CT Scan at angle  " + str(180 - angle) + "°"
        self.setStatus(statusString)


    def makeLeftSideArrows(self, angle):
        vector = [[0], [15]]  ## angle 0 vector always points up
        rotated_vector = self.rotateVector(vector, angle)
        newStartPointX = 25 + rotated_vector[0][0]
        newStartPointY = 25 + rotated_vector[1][0]
        newEndPointX = 25 - rotated_vector[0][0]
        newEndPointY = 25 - rotated_vector[1][0]
        for step in range(8):
            canvasA1 = Canvas(self.mainframe, width=50, height=50, bg="gainsboro", bd=0, highlightthickness=0, relief='ridge')
            canvasA1.place(x=0, y=30 + step * 50)
            blackLine = canvasA1.create_line(newStartPointX, newStartPointY, newEndPointX, newEndPointY, tags=("line",), arrow="last", fill="black")


    def makeRightSideArrows(self, angle):
        vector = [[0], [15]]  ## angle 0 vector always points up
        rotated_vector = self.rotateVector(vector, angle)
        newStartPointX = 25 + rotated_vector[0][0]
        newStartPointY = 25 + rotated_vector[1][0]
        newEndPointX = 25 - rotated_vector[0][0]
        newEndPointY = 25 - rotated_vector[1][0]
        for step in range(8):
            canvasA1 = Canvas(self.mainframe, width=50, height=50, bg="gainsboro", bd=0, highlightthickness=0, relief='ridge')
            canvasA1.place(x=455, y=30 + step * 50)
            blackLine = canvasA1.create_line(newStartPointX, newStartPointY, newEndPointX, newEndPointY, tags=("line",), arrow="last", fill="black")

    def rotateVector(self, vector, angle):
        angleRad = np.deg2rad(angle)
        RotationMatrix = np.matrix([[np.cos(angleRad), -1 * np.sin(angleRad)], [np.sin(angleRad), np.cos(angleRad)]])
        #print(RotationMatrix)
        outputVectorDouble = RotationMatrix * vector
        (N, M) = outputVectorDouble.shape
        outputVector = np.zeros((N, M), np.int)
        for i in range(N):
            for j in range(M):
                outputVector[i][j] = np.round(outputVectorDouble[i][j])
        return outputVector



# start Project GUI
root = Tk()

p = ProjectUI(root)

root.mainloop()

