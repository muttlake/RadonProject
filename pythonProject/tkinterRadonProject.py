from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import *
import cv2
import numpy as np
from CTScan import CTScan



class ProjectUI:

    inputImageLabel = None
    statusLabel = None
    inputImage = None    # cv2 image
    ctAcquisitionImage = None  # cv2 image
    ctAcquisitionImageLabel = None

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

        ctScanButton = Button(toolbar, text="CT Scan", command=self.doNothing)
        ctScanButton.pack(side=RIGHT, padx=20, pady=20)

        toolbar.pack(side=TOP, fill=X)

        ## ****** Status Bar ******
        self.statusLabel = Label(root, text="Started Project GUI", bd=1, relief=SUNKEN, anchor=W)  # bd = border, anchor = West
        self.statusLabel.pack(side=BOTTOM, fill=X)

        ## ****** Main Window Frame ******
        mainFrame = Frame(root, width=1000, height=500, bg="gainsboro")  # frame is a blank widget
        mainFrame.pack()

        ## ****** Input image ******
        empty_image = cv2.imread("empty_image.jpg")
        empty_image_display = self.makeDisplayImage(empty_image)
        self.inputImageLabel = Label(mainFrame, width=400, height=400, image=empty_image_display)
        self.inputImageLabel.place(x=25, y=25)

        ## ****** Input image ******
        self.ctAcquisitionImageLabel = Label(mainFrame, width=400, height=400, image=empty_image_display)
        self.ctAcquisitionImageLabel.place(x=575, y=25)

    def setStatus(self, statusString):
        self.statusLabel.configure(text=statusString)
        self.statusLabel.text = statusString

    def getInputImage(self):
        filename = filedialog.askopenfilename()
        print("Setting input image to: ", filename)

        self.inputImage = cv2.imread(filename)
        self.inputImage = cv2.cvtColor(self.inputImage, cv2.COLOR_RGB2GRAY)

        displayImage = self.makeDisplayImage(self.inputImage)

        self.inputImageLabel.configure(image=displayImage)
        self.inputImageLabel.image = displayImage
        self.setStatus("Loaded input image.")

    def makeDisplayImage(self, cv2_image):
        disp_im = Image.fromarray(cv2_image)
        disp_im = disp_im.resize((400, 400), Image.ANTIALIAS)
        return ImageTk.PhotoImage(disp_im)

    # def getCTScan(self):
    #     """ Get CT scan using CTScan class"""
    #     if self.inputImage is not None:
    #         CT = CTScan(self.inputImage, 1)
    #         radon_transform = CT.doRadon(self.inputImage)
    #         self.ctAcquisitionImage = radon_transform
    #
    #         displayImage = self.makeDisplayImage(self.ctAcquisitionImage)
    #
    #         self.ctAcquisitionImageLabel.configure(image=displayImage)
    #         self.ctAcquisitionImageLabel.image = displayImage
    #         self.setStatus("Ran CT Scan")
    #     else:
    #         print("No input image to transform.")

    def doNothing(self):
        print("Not implemented yet.")






# start Project GUI
root = Tk()

p = ProjectUI(root)

root.mainloop()

