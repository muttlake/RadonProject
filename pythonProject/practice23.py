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



## make rotated image

lenna = cv2.imread("scanner_plot.png")
lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)

(N, M) = lenna.shape

print(lenna.shape)

#
# RotM = cv2.getRotationMatrix2D((N / 2, M / 2), 135, 1)
# rotated_image = cv2.warpAffine(lenna, RotM, (N, M))
#
# cv2.imwrite("test2image135.png", rotated_image)
#

# # start Project GUI
# root = Tk()
#
# ## ****** Main Window Frame ******
# mainframe = Frame(root, width=500, height=600, bg="gainsboro")  # frame is a blank widget
# mainframe.pack()
#
#
#
# vector = [[0],[15]]
#
# def rotateVector(vector, angle):
#     angleRad = np.deg2rad(angle)
#     RotationMatrix = np.matrix( [ [np.cos(angleRad), -1*np.sin(angleRad)], [np.sin(angleRad), np.cos(angleRad)] ] )
#     print(RotationMatrix)
#     outputVectorDouble = RotationMatrix * vector
#     (N, M) = outputVectorDouble.shape
#     outputVector = np.zeros((N, M), np.int)
#     for i in range(N):
#         for j in range(M):
#             outputVector[i][j] = np.round(outputVectorDouble[i][j])
#     return outputVector
#
# rotated_vector = rotateVector(vector, 180)
# print(rotated_vector)
#
# def makeRightSideArrows(angle):
#     vector = [[0], [15]] ## angle 0 vector always points up
#     rotated_vector = rotateVector(vector, angle)
#     newStartPointX = 25 + rotated_vector[0][0]
#     print("Rotated_X: ", newStartPointX)
#     newStartPointY = 25 + rotated_vector[1][0]
#     print("Rotated_Y: ", newStartPointY)
#     newEndPointX = 25 - rotated_vector[0][0]
#     print("Rotated_X: ", newEndPointX)
#     newEndPointY = 25 - rotated_vector[1][0]
#     print("Rotated_Y: ", newEndPointY)
#     for step in range(8):
#         canvasA1 = Canvas(mainframe, width=50, height=50, bg="gainsboro", bd=0, highlightthickness=0, relief='ridge')
#         canvasA1.place(x=0, y=30 + step * 50)
#         blackLine = canvasA1.create_line(newStartPointX, newStartPointY, newEndPointX, newEndPointY, tags=("line",), arrow="last", fill="black")
#
#
#
# makeRightSideArrows(180)
#
#
#
# root.mainloop()


