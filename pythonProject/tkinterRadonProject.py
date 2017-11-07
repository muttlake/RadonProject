from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import *
import cv2


class ProjectUI:

    inputImageLabel = None
    statusLabel = None
    inputImage = None

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

        insertButton = Button(toolbar, text="Quit", command=quit)
        insertButton.pack(side=RIGHT, padx=20, pady=20)
        toolbar.pack(side=TOP, fill=X)

        ## ****** Status Bar ******
        self.statusLabel = Label(root, text="Started Project GUI", bd=1, relief=SUNKEN, anchor=W)  # bd = border, anchor = West
        self.statusLabel.pack(side=BOTTOM, fill=X)

        ## ****** Main Window Frame ******
        mainFrame = Frame(root, width=1000, height=500, bg="gainsboro")  # frame is a blank widget
        mainFrame.pack()

        empty_image = Image.open("empty_image.jpg")
        empty_image = empty_image.resize((400, 400), Image.ANTIALIAS)
        empty_image_display = ImageTk.PhotoImage(empty_image)
        self.inputImageLabel = Label(mainFrame, image=empty_image_display, width=400, height=400)
        self.inputImageLabel.place(x=25, y=25)

    def setStatus(self, statusString):
        self.statusLabel.configure(text=statusString)
        self.statusLabel.text = statusString

    def getInputImage(self):
        filename = filedialog.askopenfilename()
        print("Setting input image to: ", filename)
        self.input_image = Image.open(filename)
        displayImage = self.input_image.resize((400, 400), Image.ANTIALIAS)
        displayImage = ImageTk.PhotoImage(displayImage)
        self.inputImageLabel.configure(image=displayImage)
        self.inputImageLabel.image = displayImage
        self.setStatus("Loaded input image.")



root = Tk()

p = ProjectUI(root)

root.mainloop()

