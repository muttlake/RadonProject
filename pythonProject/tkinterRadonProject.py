from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import *
import cv2
from Scanner import Scanner
from Scanner2D import Scanner2D



class ProjectUI:


    inputImage = None    # cv2 image
    ctAcquisitionImage = None  # cv2 image

    inputImageLabel = None
    statusLabel = None
    ctAcquisitionImageLabel = None
    ctScan1DLabel = None

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

        ctScan1DButton = Button(toolbar, text="CT Scan 1D", command=self.get1DCTScan)
        ctScan1DButton.pack(side=RIGHT, padx=20, pady=20)

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
        degree0Label.place(x=30, y=225)

        degree90Label = Label(mainFrame, text="90°")
        degree90Label.place(x=250, y=5)

        degree180Label = Label(mainFrame, text="180°")
        degree180Label.place(x=455, y=225)

        ## ****** 1D CT Scan ******
        self.ctScan1DLabel = Label(mainFrame, width=400, height=300, image=empty_image_display)
        self.ctScan1DLabel.place(x=550, y=75)

        ## ****** CT Scan Image ******
        self.ctAcquisitionImageLabel = Label(mainFrame, width=400, height=400, image=empty_image_display)
        self.ctAcquisitionImageLabel.place(x=1050, y=25)


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

    def get1DCTScan(self):
        """ Get 1D CT scan using CTScan class"""
        if self.inputImage is not None:

            Scanner1 = Scanner(self.inputImage, 1)
            Scanner1.getOneSinogram(0)

            sinogram1DImage= cv2.imread("scanner_plot.png")
            sinogram1DImage = cv2.cvtColor(sinogram1DImage, cv2.COLOR_RGB2GRAY)
            displayImage = self.makeDisplayImage(sinogram1DImage, (400, 300))

            self.ctScan1DLabel.configure(image=displayImage)
            self.ctScan1DLabel.image = displayImage
            self.setStatus("Ran 1D CT Scan at angle")
        else:
            print("No input image to do 1D transform.")

    def getCTScan(self):
        """ Get CT scan using CTScan class"""
        self.setStatus("Running Full CT Scan")
        if self.inputImage is not None:

            Scanner2 = Scanner2D(self.inputImage, 180)
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

    def doNothing(self):
        print("Not implemented yet.")






# start Project GUI
root = Tk()

p = ProjectUI(root)

root.mainloop()

