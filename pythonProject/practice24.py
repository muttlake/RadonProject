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




# start Project GUI
# root = Tk()
#
# mainframe = Frame(root, width=1500, height=1000, bg="gainsboro")  # frame is a blank widget
# mainframe.pack()
#
# canvas5 = Canvas(mainframe, width=480, height=60, bg="gainsboro", bd=0, highlightthickness=0, relief='ridge')
# canvas5.place(x=760, y=520)
# textID = canvas5.create_text(5, 30, anchor="nw", text="Python Scikit-Image Radon")
#
#
# root.mainloop()

lenna = cv2.imread("label1rot.png")
#lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)
#lenna = cv2.resize(lenna, (0,0),  fx=.452, fy=.452, interpolation=cv2.INTER_LINEAR)

(N, M, R) = lenna.shape
print("Input image shape: ", lenna.shape)



# imageTest = np.zeros((N, M), np.uint8)
#
# for row in range(N):
#     for col in range(M):
#         if row >= 160 and row <= 220:
#             if col >= 160 and col <= 220:
#                 imageTest[row][col] = 255



# (N, M) = lenna.shape



# for row in range(N):
#     for col in range(M):
#         if row + 30 <= 255:
#             rotated_matrix[row][col] = rotated_matrix[row + 30][col]
#         else:
#             rotated_matrix[row][col] = 0
#
# # for row in range(N):
# #     for col in range(M):
# #         if col - 30 < 0:
# #             rotated_matrix[row][col] = 0
# #         else:
# #             rotated_matrix[row][col] = rotated_matrix[row][col - 30]
#
# cv2.imwrite("testBox.png", rotated_matrix)

#
# def printUnsignedImage(self, image):
#     (N, M) = image.shape
#     if N < 20:
#         for i in range(N):
#             for j in range(M):
#                 print('{: <8}'.format(image[i][j]), "  ", end=""),
#             print("", end="\n"),
#     else:
#         print("Image too large to print.")
#
# def printUnsignedImage(image):
#     (N, M) = image.shape
#     if N < 20:
#         for i in range(N):
#             for j in range(M):
#                 print('{: <8}'.format(image[i][j]), "  " , end=""),
#             print("", end="\n"),
#     else:
#         print("Image too large to print.")
#
# def printImage(image):
#     (N, M) = image.shape
#     if N < 20:
#         for i in range(N):
#             for j in range(M):
#                 print("%.2f" % image[i][j], "  " , end=""),
#             print("", end="\n"),
#     else:
#         print("Image too large to print.")
#
#
# def printComplexImage(image):
#     (N, M) = image.shape
#     if N < 20:
#         for i in range(N):
#             for j in range(M):
#                 print('{: <16}'.format('{:.2f}'.format(image[i][j])) , end=""),
#             print("", end="\n"),
#     else:
#         print("Image too large to print.")
#
#
#
# def makeDisplayImage(filterMatrix):
#     (N, M) = filterMatrix.shape
#     display_image = np.zeros((N, M), np.uint8)
#     for i in range(N):
#         for j in range(M):
#             display_image[i][j] = round(255.0 * filterMatrix[i][j])
#     return display_image
#
#
#
# print("Printing lenna input image.")
# print(lenna)
#
#
# # DO radon
# Scanner2 = Scanner2D(lenna, 20)
# Scanner2.radon2D()
#
# rawRadonMatrix = Scanner2.getRawRadonMatrix()
# anglesArray = Scanner2.getRadonAnglesArray()
#
# print("\n\nPrinting angles array.")
# print(anglesArray)
#
# print("\n\nPrinting raw radon matrix.")
# print(rawRadonMatrix)
#
# # DO backprojection
# StepWiseBackprojector = CTScanBackprojector(lenna, rawRadonMatrix, anglesArray)
# currentAngleIndex = 0
#
#
# for angle in anglesArray:
#     print("\n\nThe angle is: ", angle)
#     StepWiseBackprojector.stepwiseBackprojection(currentAngleIndex)
#     radon_backprojection = StepWiseBackprojector.getRawBackprojectionMatrix()
#     currentAngleIndex +=1
#
#     print("\n\nPrinting radon backprojection matrix.")
#     printImage(radon_backprojection)
#

