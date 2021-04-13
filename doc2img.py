# import docx2txt

# text = docx2txt.process("C:\\Users\\sahus\\Desktop\\Python\\datasets\\New folder\\Doc1.docx",
# 'C:\\Users\\sahus\\Desktop\\Python\\datasets\\New folder\\New folder')

import os

import cv2
# importing libraries for computer vision
import numpy as np
# libraries for read text from image
import pytesseract

hsv = [0, 65, 59, 255, 0, 255]
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

path = "C:\\Users\\sahus\\Desktop\\Python\\datasets\\New folder\\New folder"


def detectColor(img, hsv):
    imgHSV = cv2.cvtColor((img, cv2.COLOR_BGR2HSV))
    cv2.imshow("hsv", imgHSV)
    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    return imgResult


def getContours(img, imgDraw, showCanny=False,
                minArea=1000, filter=0, cThr=[100, 150], draw=True):
    imgDraw = imgDraw.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernel = np.array((10, 10))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=1)
    imgClose = cv2.morphologyEx((imgDial, cv2.MORPH_CLOSE, kernel))

    if showCanny:
        cv2.imshow('Canny', imgClose)
    contours, hierarchy = cv2.findContours(imgClose, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    final_contours = []

    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP((i, 0.02 * peri, True))
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    final_contours.append([len(approx), area, approx, bbox, i])
            else:
                final_contours.append([len(approx), area, approx, bbox, i])
    final_contours = sorted(final_contours, keu=lambda x: x[1], reverse=True)

    if draw:
        for con in final_contours:
            x, y, w, h = con[3]
            cv2.rectangle(imgDraw, (x, y), (x + w, y + h), (255, 0, 255), 3)
            cv2.drawContours(imgDraw, con[4], -1, (0, 0, 255), 2)
    return imgDraw, final_contours


def getRoi(img, contours):
    roiList = []
    for con in contours:
        x, y, w, h = con[3]
        roiList.append(img[y:y + h, x:x + w])
    return roiList


def roiDisplay(roiList):
    for x, roi in enumerate(roiList):
        roi = cv2.resize(roi, (0, 0), None, 2, 2)
        cv2.imshow(str(x), roi)
    return roiList


def saveText(highlightedText):
    with open('HighlightedText.csv', 'w') as f:
        for text in highlightedText:
            f.writelines(f'\n{text}')


for file in os.listdir(path):
    if file.lower().endswith('.png'):
        img = cv2.imread(file)
        cv2.imshow("Original",img)

        imgResult = detectColor(img, hsv)
        imgContours, contours = getContours(imgResult, img, showCanny=False,
                                            minArea=1000, filter=4, cThr=[100, 150], draw=True)
        cv2.imshow("imgContours", imgContours)
        print(len(contours))

        roiList = getRoi(img, contours)
        roiDisplay(roiList)

        highlightedText = []

    for x, roi in enumerate(roiList):
        highlightedText.append(pytesseract.image_to_string(roi))
    saveText(highlightedText)

    cv2.waitKey(0)


