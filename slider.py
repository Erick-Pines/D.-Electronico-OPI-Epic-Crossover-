 
from __future__ import division
import cv2
import numpy as np
import time
 
def nothing(*arg):
        pass
 
i = int(input())

high_val = 230
low_val = 40
high_sat = 255
low_sat = 100

colors = [
    # Definir el rango de colores en HSV (Matiz, Saturacion, Luminosidad)
    ([45, 45, 40, 90, 150, 245]),   # 0 = Verde
    ([0, 120, 0, 5, 255, 150]),     # 1 = Rojo
    ([25, 70, 150, 45, 140, 200]),  # 2 = Amarillo
    ([90, 70, 150, 120, 200, 210]), # 3 = Azul
    ([10, 100, 50, 25, 200, 180])   # 4 = Naranja  
]

cv2.namedWindow('colorTest')
# Lower range colour sliders.
cv2.createTrackbar('lowHue', 'colorTest', colors[i][0], 255, nothing)
cv2.createTrackbar('lowSat', 'colorTest', colors[i][1], 255, nothing)
cv2.createTrackbar('lowVal', 'colorTest', colors[i][2], 255, nothing)
# Higher range colour sliders.
cv2.createTrackbar('highHue', 'colorTest', colors[i][3], 255, nothing)
cv2.createTrackbar('highSat', 'colorTest', colors[i][4], 255, nothing)
cv2.createTrackbar('highVal', 'colorTest', colors[i][5], 255, nothing)
 
frame = cv2.imread('img/guitar-hero.jpg')
#cap = cv2.VideoCapture(0)

while True:
    # Get HSV values from the GUI sliders.
    #_, frame = cap.read()
    
    lowHue = cv2.getTrackbarPos('lowHue', 'colorTest')
    lowSat = cv2.getTrackbarPos('lowSat', 'colorTest')
    lowVal = cv2.getTrackbarPos('lowVal', 'colorTest')
    highHue = cv2.getTrackbarPos('highHue', 'colorTest')
    highSat = cv2.getTrackbarPos('highSat', 'colorTest')
    highVal = cv2.getTrackbarPos('highVal', 'colorTest')
 
    # Show the original image.
    cv2.imshow('frame', frame)
    
    # Blur methods available, comment or uncomment to try different blur methods.
    frameBGR = cv2.GaussianBlur(frame, (7, 7), 0)
    #frameBGR = cv2.medianBlur(frameBGR, 7)
    #frameBGR = cv2.bilateralFilter(frameBGR, 15 ,75, 75)
    """kernal = np.ones((15, 15), np.float32)/255
    frameBGR = cv2.filter2D(frameBGR, -1, kernal)"""
    
    # Show blurred image.
    #cv2.imshow('blurred', frameBGR)
        
    # HSV (Hue, Saturation, Value).
    # Convert the frame to HSV colour model.
    hsv = cv2.cvtColor(frameBGR, cv2.COLOR_BGR2HSV)
        
    # HSV values to define a colour range.
    colorLow = np.array([lowHue,lowSat,lowVal])
    colorHigh = np.array([highHue,highSat,highVal])
    mask = cv2.inRange(hsv, colorLow, colorHigh)
    # Show the first mask
    #cv2.imshow('mask-plain', mask)
 
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)

    # Show morphological transformation mask
    #cv2.imshow('mask', mask)
        
    # Put mask over top of the original image.
    result = cv2.bitwise_and(frame, frame, mask = mask)

    # Show final output image
    cv2.imshow('colorTest', mask)
    cv2.imshow('result', result)
        
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()