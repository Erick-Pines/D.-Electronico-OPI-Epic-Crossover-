import cv2
import numpy as np

colors = [
    # Definir el rango de colores en HSV (Matiz, Saturacion, Luminosidad)
    (np.array([45, 45, 40]),    np.array([90, 150, 245])),  # 0 = Verde
    (np.array([0, 120, 0]),     np.array([5, 255, 150])),   # 1 = Rojo
    (np.array([25, 70, 150]),   np.array([45, 140, 200])),  # 2 = Amarillo
    (np.array([90, 70, 150]),   np.array([120, 200, 210])), # 3 = Azul
    (np.array([10, 100, 50]),    np.array([25, 200, 180]))  # 4 = Naranja  
]
x = input()
lower = colors[x][0]
upper = colors[x][1]

cap = cv2.VideoCapture(0)
while True:
    # Dividir por frame
    _, frame = cap.read()
    # Convertir de BGR (Blue, Green, Red) a HSV (Hue, Saturation, Value)
    blur = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)   

    # Hacer una mascara con solo los pixeles dentro del rango de cada color
    mask = cv2.inRange(hsv, lower, upper)
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
    # Dejar la mascara con los colores originales
    final = cv2.bitwise_and(frame,frame, mask= mask)
    # Imprimir video y mascara
    
    cv2.imshow('frame',frame) #Original
    cv2.imshow('final',final) #Color

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()