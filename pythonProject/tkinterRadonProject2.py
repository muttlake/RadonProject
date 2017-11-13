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
from CTScanBackprojector import CTScanBackprojector

class ProjectUI:


    inputImage = None    # cv2 image
    numAngles = None
    ctAcquisitionImage = None  # cv2 image
    currentAngleIndex = None

    ctRawRadonMatrix = None
    radonAnglesArray = None

    inputImageLabel = None
    statusLabel = None
    ctAcquisitionImageLabel = None
    ctBackProjectionLabel = None
    scikitRadonAndIradonLabel = None
    ctScan1DLabel = None

    numAnglesTextBox = None
    angleIncrementLabel = None

    StepWiseScanner2D = None
    StepWiseBackprojector = None
    changeOccurred = False

    mainframe = None

    def __init__(self, master): # master means root or main window

        ## ****** Main Menu ******
        menu = Menu(master)

        master.config(menu=menu)
        subMenu = Menu(menu)

        menu.add_cascade(label="File", menu=subMenu)
        subMenu.add_command(label="Exit", command=quit)

        ## ****** Top Toolbar ******
        toolbar = Frame(master, bg="azure3")

        insertButton = Button(toolbar, text="Get Image", command=self.getInputImage)
        insertButton.pack(side=LEFT, padx=20, pady=20)

        quitButton = Button(toolbar, text="Quit", command=quit)
        quitButton.pack(side=RIGHT, padx=20, pady=20)



        ctScanButton = Button(toolbar, text="CT Scan Full", command=self.getCTScan)
        ctScanButton.pack(side=RIGHT, padx=20, pady=20)

        ctStepwiseScanButton = Button(toolbar, text="CT Scan Step", command=self.doStepwiseCTScan)
        ctStepwiseScanButton.pack(side=RIGHT, padx=20, pady=20)

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

        degree0Label = Label(self.mainframe, text="0°", bg="gainsboro")
        degree0Label.place(x=225, y=430)


        ## ****** Make Arrow above 1D Radon Transform ******
        self.makeArrows(0)

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
        numAnglesLabel.place(x = 30, y=470)
        self.numAnglesTextBox = Text(self.mainframe, height=1, width=5, bg="light gray")
        self.numAnglesTextBox.place(x=425, y=470)
        buttonCommitNumAngles = Button(self.mainframe, height=1, width=10, text="Commit",
                                       command=self.retrieve_num_angles_input)
        buttonCommitNumAngles.place(x=400, y=495)
        self.angleIncrementLabel = Label(self.mainframe, text="", bg="gainsboro", fg="red")
        self.angleIncrementLabel.place(x=30, y=495)

        ## ****** BackProjection Image ******
        self.ctBackProjectionLabel = Label(self.mainframe, width=400, height=400, image=empty_image_display)
        self.ctBackProjectionLabel.place(x=50, y=575)

        ## ****** SciKit Radon and IRadon BackProjection Image ******
        self.scikitRadonAndIradonLabel = Label(self.mainframe, width=640, height=480, image=empty_image_display)
        self.scikitRadonAndIradonLabel.place(x=835, y=515)


        ## ****** Bottom Toolbar ******
        toolbarBottom = Frame(master, bg="azure3")

        backprojectorSKIButton = Button(toolbarBottom, text="IRadon Scikit Full", command=self.doNothing)
        backprojectorSKIButton.pack(side=RIGHT, padx=20, pady=20)

        ctScanSKIButton = Button(toolbarBottom, text="CT Scan Scikit Full", command=self.getCTScanSKI)
        ctScanSKIButton.pack(side=RIGHT, padx=20, pady=20)

        backprojectorButton = Button(toolbarBottom, text="Backproject Full", command=self.doFullBackprojection)
        backprojectorButton.pack(side=LEFT, padx=20, pady=20)

        stepwiseBackprojectorButton = Button(toolbarBottom, text="Backproject Step", command=self.doStepwiseBackprojection)
        stepwiseBackprojectorButton.pack(side=LEFT, padx=20, pady=20)

        toolbarBottom.pack(side=BOTTOM, fill=X)

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
            numAngle2 = 10  # default number of angles
            if self.numAngles is not None:
                numAngle2 = int(self.numAngles)
            else:
                angleIncrement = np.float(180) / np.float(numAngle2)
                outputString = "Setting the angle increment to  " + str(angleIncrement) + "°"
                self.angleIncrementLabel.config(text=outputString)
                self.angleIncrementLabel.text = outputString

            Scanner2 = Scanner2D(self.inputImage, numAngle2)
            Scanner2.radon2D()
            radon_transf = Scanner2.getRadonImage()

            self.ctRawRadonMatrix = Scanner2.getRawRadonMatrix()
            self.radonAnglesArray = Scanner2.getRadonAnglesArray()
            print(radon_transf.shape)

            displayImage = self.makeDisplayImage(radon_transf, (640, 480))

            self.makeArrows(180)

            self.ctAcquisitionImageLabel.configure(image=displayImage)
            self.ctAcquisitionImageLabel.image = displayImage
            self.setStatus("Ran Full CT Scan")
            # Do 1D CT Scan
            self.do1DCTScan(0)
        else:
            self.setStatus("Please choose an input image.")

    def getCTScanSKI(self):
        """ Get CT scan using CTScan class"""
        if self.inputImage is not None:
            numAngles2 = 10  # default number of angles
            if self.numAngles is not None:
                numAngles2 = int(self.numAngles)
            else:
                angleIncrement = np.float(180) / np.float(numAngles2)
                outputString = "Setting the angle increment to  " + str(angleIncrement) + "°"
                self.angleIncrementLabel.config(text=outputString)
                self.angleIncrementLabel.text = outputString


            #rint("Number of angles in getCTScanSKI: ", numAngles2)
            Scanner2 = Scanner2DSKI(self.inputImage, numAngles2)
            Scanner2.radon2D()
            Scanner2.saveRadon2DImage()

            radon_transf = cv2.imread("radon2D_Image.png")
            radon_transf = cv2.cvtColor(radon_transf, cv2.COLOR_RGB2GRAY)
            #print("Scanner2DSKI radon_transf shape: ", radon_transf.shape)
            displayImage = self.makeDisplayImage(radon_transf, (640, 480))

            self.makeArrows(180)

            self.scikitRadonAndIradonLabel.configure(image=displayImage)
            self.scikitRadonAndIradonLabel.image = displayImage
            self.setStatus("Ran SciKit CT Scan for all Angles")
            # Do 1D CT Scan
            self.do1DCTScan(0)
        else:
            self.setStatus("Please choose an input image.")


    def doStepwiseCTScan(self):
        """Step through each angle and do CT scan, display 1D and 2D stepwise results"""
        if self.inputImage is None:
            self.setStatus("Please choose an input image.")
            return
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
            self.makeArrows(0)

        anglesArray = self.StepWiseScanner2D.getAnglesArray()

        angle = anglesArray[self.currentAngleIndex]

        #Do 1D CT Scan
        self.do1DCTScan(angle)

        #Rotate Arrows
        self.makeArrows(angle)

        #Make 2D Stepwise Scan
        self.StepWiseScanner2D.stepwiseRadon2D(self.currentAngleIndex)
        self.StepWiseScanner2D.startOverStepWise = False
        self.currentAngleIndex += 1
        self.currentAngleIndex = self.currentAngleIndex % len(anglesArray)
        current_radon_transf = self.StepWiseScanner2D.getRadonImage()

        displayImage = self.makeDisplayImage(current_radon_transf, (640, 480))

        self.ctAcquisitionImageLabel.configure(image=displayImage)
        self.ctAcquisitionImageLabel.image = displayImage

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
        rotated_vector = self.rotateVector(vector, angle*-1)
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
        rotated_vector = self.rotateVector(vector, angle*-1)
        newStartPointX = 25 + rotated_vector[0][0]
        newStartPointY = 25 + rotated_vector[1][0]
        newEndPointX = 25 - rotated_vector[0][0]
        newEndPointY = 25 - rotated_vector[1][0]
        for step in range(8):
            canvasA1 = Canvas(self.mainframe, width=50, height=50, bg="gainsboro", bd=0, highlightthickness=0, relief='ridge')
            canvasA1.place(x=455, y=30 + step * 50)
            blackLine = canvasA1.create_line(newStartPointX, newStartPointY, newEndPointX, newEndPointY, tags=("line",), arrow="last", fill="black")

    def makeLowerLeftSideArrows(self, angle):
        vector = [[0], [15]]  ## angle 0 vector always points up
        rotated_vector = self.rotateVector(vector, angle*-1 + 180)
        newStartPointX = 25 + rotated_vector[0][0]
        newStartPointY = 25 + rotated_vector[1][0]
        newEndPointX = 25 - rotated_vector[0][0]
        newEndPointY = 25 - rotated_vector[1][0]
        for step in range(8):
            canvasA2 = Canvas(self.mainframe, width=50, height=50, bg="gainsboro", bd=0, highlightthickness=0, relief='ridge')
            canvasA2.place(x=0, y=580 + step * 50)
            blackLine = canvasA2.create_line(newStartPointX, newStartPointY, newEndPointX, newEndPointY, tags=("line",), arrow="last", fill="black")


    def makeLowerRightSideArrows(self, angle):
        vector = [[0], [15]]  ## angle 0 vector always points up
        rotated_vector = self.rotateVector(vector, angle*-1 + 180)
        newStartPointX = 25 + rotated_vector[0][0]
        newStartPointY = 25 + rotated_vector[1][0]
        newEndPointX = 25 - rotated_vector[0][0]
        newEndPointY = 25 - rotated_vector[1][0]
        for step in range(8):
            canvasA2 = Canvas(self.mainframe, width=50, height=50, bg="gainsboro", bd=0, highlightthickness=0, relief='ridge')
            canvasA2.place(x=455, y=580 + step * 50)
            blackLine = canvasA2.create_line(newStartPointX, newStartPointY, newEndPointX, newEndPointY, tags=("line",), arrow="last", fill="black")

    def makeArrows(self, angle):
        """Rotate arrows on gui by angle"""
        #Arrows for input image
        self.makeRightSideArrows(angle)
        self.makeLeftSideArrows(angle)

        # Arrows for backprojection
        self.makeLowerRightSideArrows(angle)
        self.makeLowerLeftSideArrows(angle)

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

    def doFullBackprojection(self):
        if self.inputImage is None:
            self.setStatus("Please choose an input image.")
            return

        if self.ctRawRadonMatrix is None:
            self.getCTScan()

        numAngle2 = 10
        if self.numAngles is not None:
            numAngle2 = int(self.numAngles)
        else:
            angleIncrement = np.float(180) / np.float(numAngle2)
            outputString = "Setting the angle increment to  " + str(angleIncrement) + "°"
            self.angleIncrementLabel.config(text=outputString)
            self.angleIncrementLabel.text = outputString

        if self.changeOccurred:
            self.getCTScan()
            self.changeOccurred = False
            self.makeArrows(0)

        FullBackprojector = CTScanBackprojector(self.inputImage, self.ctRawRadonMatrix, self.radonAnglesArray)
        FullBackprojector.doFullBackprojection()
        radon_backprojection_image = FullBackprojector.getRadonImage()

        #Rotate Arrows
        self.makeArrows(180)

        displayImage = self.makeDisplayImage(radon_backprojection_image, (400, 400))

        self.ctBackProjectionLabel.configure(image=displayImage)
        self.ctBackProjectionLabel.image = displayImage
        statusString = "Ran Full Backprojection for all angles."
        self.setStatus(statusString)
        self.changeOccurred = True


    def doStepwiseBackprojection(self):
        """Step through each angle and do CT scan, display 1D and 2D stepwise results"""
        if self.inputImage is None:
            self.setStatus("Please choose an input image.")
            return

        if self.ctRawRadonMatrix is None:
            self.getCTScan()

        numAngle2 = 10
        if self.numAngles is not None:
            numAngle2 = int(self.numAngles)
        else:
            angleIncrement = np.float(180) / np.float(numAngle2)
            outputString = "Setting the angle increment to  " + str(angleIncrement) + "°"
            self.angleIncrementLabel.config(text=outputString)
            self.angleIncrementLabel.text = outputString

        if self.StepWiseBackprojector is None or self.changeOccurred:
            self.getCTScan()
            self.StepWiseBackprojector = CTScanBackprojector(self.inputImage, self.ctRawRadonMatrix, self.radonAnglesArray)
           #self.StepWiseBackprojector.cleanBackprojectionMatrix()
            #self.StepWiseScanner2D.startOverStepWise = True
            self.currentAngleIndex = 0
            self.changeOccurred = False
            self.makeArrows(0)

        if self.currentAngleIndex >= len(self.radonAnglesArray):
            self.StepWiseBackprojector.cleanBackprojectionMatrix()
            self.currentAngleIndex = self.currentAngleIndex % len(self.radonAnglesArray)

        angle = self.radonAnglesArray[self.currentAngleIndex]

        #Make 2D Stepwise Scan
        self.StepWiseBackprojector.stepwiseBackprojection(self.currentAngleIndex)
        radon_backprojection_image = self.StepWiseBackprojector.getRadonImage()


        self.currentAngleIndex += 1

        #Rotate Arrows
        self.makeArrows(angle)

        displayImage = self.makeDisplayImage(radon_backprojection_image, (400, 400))

        self.ctBackProjectionLabel.configure(image=displayImage)
        self.ctBackProjectionLabel.image = displayImage
        statusString = "Ran Stepwise Backprojection at angle  " + str(angle) + "°"
        self.setStatus(statusString)





# start Project GUI
root = Tk()

p = ProjectUI(root)

root.mainloop()

