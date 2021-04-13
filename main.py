from utils import *
import pytesseract


path = 'C:\\Users\\sahus\\Desktop\\Python\\datasets\\New folder\\New folder\\image1.png'
hsv = [0,179,0,114,194,255]
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#### Step 1 ####
img = cv2.imread(path)
# cv2.imshow("Original",img)
#### Step 2 ####
imgResult = detectColor(img, hsv)
#### Step 3 & 4 ####
imgContours, contours = getContours(imgResult, img, showCanny=True,
                                    minArea=1000, filter=4,
                                    cThr=[200, 200], draw=True)
cv2.imshow("imgContours",imgContours)
print(len(contours))

#### Step 5 ####
roiList = getRoi(img, contours)
#cv2.imshow("TestCrop",roiList[2])
roiDisplay(roiList)

#### Step 6 ####
highlightedText = []
for x, roi in enumerate(roiList):
    print(pytesseract.image_to_string(img))
    highlightedText.append(pytesseract.image_to_string(img))

saveText(highlightedText)

#imgStack = stackImages(0.7, ([img, imgResult, imgContours]))
#cv2.imshow("Stacked Images", imgStack)

cv2.waitKey(0)
