import cv2
import numpy as np

height = 286 #480
width = 468 #640
visited = np.zeros((height, width), dtype=bool)

dx=[0, 1, 0, -1]
dy=[-1, 0, 1, 0]
colors = [
    # Definir el rango de colores en HSV (Matiz, Saturacion, Luminosidad)
    (np.array([45, 45, 40]),    np.array([90, 150, 245])),  # 0 = Verde
    (np.array([0, 120, 0]),     np.array([5, 255, 150])),   # 1 = Rojo
    (np.array([25, 70, 150]),   np.array([45, 140, 200])),  # 2 = Amarillo
    (np.array([90, 70, 150]),   np.array([120, 200, 210])), # 3 = Azul
    (np.array([10, 100, 50]),    np.array([25, 200, 180]))  # 4 = Naranja  
]
n = input()
lower = colors[n][0]
upper = colors[n][1]




def contar(mask,x,y):
    if x<0 or y<0 or x==width or y==height :
        return 0
    if mask[y][x] == 0:
        return 0
    if visited[y][x]==1:
        return 0
    visited[y][x]=1
    c=1
    for i in xrange(0,4):
        c+=contar(mask, x+dx[i], y+dy[i])
    return c

#cap = cv2.VideoCapture(0)
frame = cv2.imread('img/guitar-hero.jpg')

while True:
    # Convertir de BGR (Blue, Green, Red) a HSV (Hue, Saturation, Value)
    #_, frame = cap.read()
    n = 0
    c = 0
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
    cv2.imshow('final',mask) #Color
    for i in xrange(0,height):
        for j in xrange(0,width):
            if mask[i][j] and visited[i][j]==0 :
                n+=contar(mask,j,i)
                c+=1

    print(n, c)
    visited = np.zeros((height, width), dtype=bool)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()