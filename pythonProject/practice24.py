import cv2
from Scanner import Scanner
from Scanner2D import Scanner2D
from Scanner2DSKI import Scanner2DSKI
from CTScanBackprojector import CTScanBackprojector


lenna = cv2.imread("test2Image135small.png")
lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)
#lenna = cv2.resize(lenna, (0,0),  fx=.0625, fy=.0625, interpolation=cv2.INTER_LINEAR)
#cv2.imwrite("test2Image135small.png", lenna)

(N, M) = lenna.shape
print("Input image shape: ", lenna.shape)


def printUnsignedImage(self, image):
    (N, M) = image.shape
    if N < 20:
        for i in range(N):
            for j in range(M):
                print('{: <8}'.format(image[i][j]), "  ", end=""),
            print("", end="\n"),
    else:
        print("Image too large to print.")

def printUnsignedImage(image):
    (N, M) = image.shape
    if N < 20:
        for i in range(N):
            for j in range(M):
                print('{: <8}'.format(image[i][j]), "  " , end=""),
            print("", end="\n"),
    else:
        print("Image too large to print.")

def printImage(image):
    (N, M) = image.shape
    if N < 20:
        for i in range(N):
            for j in range(M):
                print("%.2f" % image[i][j], "  " , end=""),
            print("", end="\n"),
    else:
        print("Image too large to print.")


def printComplexImage(image):
    (N, M) = image.shape
    if N < 20:
        for i in range(N):
            for j in range(M):
                print('{: <16}'.format('{:.2f}'.format(image[i][j])) , end=""),
            print("", end="\n"),
    else:
        print("Image too large to print.")



def makeDisplayImage(filterMatrix):
    (N, M) = filterMatrix.shape
    display_image = np.zeros((N, M), np.uint8)
    for i in range(N):
        for j in range(M):
            display_image[i][j] = round(255.0 * filterMatrix[i][j])
    return display_image



print("Printing lenna input image.")
print(lenna)


# DO radon
Scanner2 = Scanner2D(lenna, 20)
Scanner2.radon2D()

rawRadonMatrix = Scanner2.getRawRadonMatrix()
anglesArray = Scanner2.getRadonAnglesArray()

print("\n\nPrinting angles array.")
print(anglesArray)

print("\n\nPrinting raw radon matrix.")
print(rawRadonMatrix)

# DO backprojection
StepWiseBackprojector = CTScanBackprojector(lenna, rawRadonMatrix, anglesArray)
currentAngleIndex = 0


for angle in anglesArray:
    print("\n\nThe angle is: ", angle)
    StepWiseBackprojector.stepwiseBackprojection(currentAngleIndex)
    radon_backprojection = StepWiseBackprojector.getRawBackprojectionMatrix()
    currentAngleIndex +=1

    print("\n\nPrinting radon backprojection matrix.")
    printImage(radon_backprojection)

