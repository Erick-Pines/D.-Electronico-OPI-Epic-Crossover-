import cv2
import numpy as np

height = 286 #480 pixeles en grabacion
width = 468 #640 
visited = np.zeros((height, width), dtype=bool) # Arreglo de visitados

dx=[0, 1, 0, -1]
dy=[-1, 0, 1, 0]
colors = [
    # Definir el rango de colores en HSV (Matiz, Saturacion, Luminosidad)
    (np.array([45, 45, 40]),    np.array([90, 150, 245])),  # 0 = Verde
    (np.array([173, 0, 148]),   np.array([255, 255, 255])), # 1 = Rojo
    (np.array([20, 22, 105]),   np.array([40, 115, 255])),  # 2 = Amarillo
    (np.array([100, 35, 91]),   np.array([115, 255, 255])), # 3 = Azul
    (np.array([10, 0, 59]),     np.array([17, 255, 175])),  # 4 = Naranja
    (np.array([0, 0, 143]),     np.array([190, 10, 255]))   # 5 = Blanco  
]
n = input()
lower = colors[n][0]
upper = colors[n][1]

def contar(mask,x,y):
    if x<0 or y<0 or x>=width or y>=height : # Si pasa los limites
        return 0
    if mask[y][x] == 0: #Si es negro
        return 0
    if visited[y][x]==1: #Si ya fue visitado
        return 0
    visited[y][x]=1
    c=1
    for i in xrange(0,4):
        c+=contar(mask, x+dx[i], y+dy[i]) # Visitar pixeles adyacentes ^ > v <
    return c # Regresar cantidad de pixeles blancos

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

    # Barrido en la mascara
    for i in xrange(0,height):
        for j in xrange(0,width):
            if mask[i][j] and visited[i][j]==0 :
                n+=contar(mask,j,i) # Llamar busqueda en profundidad
                c+=1 # Contar objetos del color

    print(n, c)
    visited = np.zeros((height, width), dtype=bool) #Inicializar arreglo de visitados

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()