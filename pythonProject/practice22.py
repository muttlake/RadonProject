from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import *
from matplotlib import pyplot as plt
import numpy as np
import cv2
from CTScan import CTScan

lenna = cv2.imread("testImage2.png")
lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)
print(lenna.shape)
cv2.imshow("Lenna", lenna)
cv2.waitKey()

CT = CTScan(lenna, 60)

values = CT.onePassRadon(lenna)

radonTransform = CT.doRadon(lenna)


print(values)

plt.plot(values)
plt.show()

# pil_im = Image.fromarray(lenna)
# pil_im = pil_im.resize((400, 400), Image.ANTIALIAS)
# pil_im.show()








cv2.waitKey()



