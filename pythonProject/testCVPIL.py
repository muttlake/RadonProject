from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import *
import cv2


lenna = cv2.imread("SheppLogan_Phantom.png")
print(lenna.shape)
lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)

pil_im = Image.fromarray(lenna)
pil_im = pil_im.resize((400, 400), Image.ANTIALIAS)
pil_im.show()

cv2.imshow("Lenna", lenna)

cv2.waitKey()
