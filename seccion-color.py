import cv2
import numpy as np

height = 286 #480
width = 468 #640
visited = np.zeros((height, width), dtype=bool)
boton = [0, 0, 0, 0, 0]

colors = [
    # Definir el rango de colores en HSV (Matiz, Saturacion, Luminosidad)
    (np.array([45, 45, 40]),    np.array([90, 150, 245])),  # 0 = Verde
    (np.array([173, 0, 148]),   np.array([255, 255, 255])), # 1 = Rojo
    (np.array([20, 22, 105]),   np.array([40, 115, 255])),  # 2 = Amarillo
    (np.array([100, 35, 91]),   np.array([115, 255, 255])), # 3 = Azul
    (np.array([10, 0, 59]),     np.array([17, 255, 175])),  # 4 = Naranja
    (np.array([0, 0, 143]),     np.array([190, 10, 255]))   # 5 = Blanco  
]
seccion = [
    (211, 117, 238, 172),   # 0 = Verde
    (211, 173, 238, 228),   # 1 = Rojo
    (211, 231, 238, 286),   # 2 = Amarillo
    (211, 288, 238, 347),   # 3 = Azul
    (211, 352, 238, 404),   # 4 = Naranja
]

#cap = cv2.VideoCapture(0)
frame = cv2.imread('img/guitar-hero.jpg')

while True:
    
    #_, frame = cap.read()
    blur = cv2.GaussianBlur(frame, (7, 7), 0)
    # Convertir de BGR (Blue, Green, Red) a HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)   

    mask = 0
    for i in xrange(0,5):
        # Hacer una mascara con solo los pixeles dentro del rango de cada color
        current = cv2.inRange(hsv, colors[i][0], colors[i][1])
        kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        current = cv2.morphologyEx(current, cv2.MORPH_CLOSE, kernal)
        current = cv2.morphologyEx(current, cv2.MORPH_OPEN, kernal)

        y = seccion[i][0]
        while y <= seccion[i][2]:
            x = seccion[i][1]
            while x <= seccion[i][3]:
                if current[y][x]:
                    boton[i]=1
                    break
                x+=1
            y+=1

        # Unirla con las mascaras anteriores
        mask += current

    # Dejar la mascara con los colores originales
    final = cv2.bitwise_and(frame,frame, mask= mask)
    # Imprimir video y mascara
    
    cv2.imshow('frame',frame) #Original
    cv2.imshow('final',mask) #Color
    """
    x1 = 1000
    y1 = 1000
    x2 = 0
    y2 = 0
    for i in xrange(0,height):
        for j in xrange(0,width):
            if mask[i][j] and visited[i][j]==0 :
                if i < y1:
                    y1 = i
                if j < x1:
                    x1 = j
                if i > y2:
                    y2 = i
                if j > x2:
                    x2 = j
    """
    print(boton)

    boton = [0, 0, 0, 0, 0]
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()