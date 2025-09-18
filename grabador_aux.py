import cv2 as cv
import numpy as np
import pyautogui
from threading import Lock
from PIL import Image, ImageTk

# Variables de control con protección de hilos
paro = False
lock = Lock()
current_frame = None
frame_lock = Lock()

def detener():
    global paro, lock
    with lock:
        paro = True

def get_current_frame():
    global current_frame, frame_lock
    with frame_lock:
        return current_frame

def grabador(resolucion=(1920, 1080), fps=60.0, archivo_nombre="Grabado archivo.avi"):
    global paro, lock, current_frame, frame_lock
    
    # Reiniciar el estado de paro
    with lock:
        paro = False
    
    codec = cv.VideoWriter_fourcc(*'MPEG')
    out = cv.VideoWriter(archivo_nombre, codec, fps, resolucion)
    
    try:
        while True:
            # Verificar si se debe detener
            with lock:
                if paro:
                    break
            
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            
            # Guardar el frame actual para la vista previa
            with frame_lock:
                current_frame = cv.resize(frame, (640, 360))  # Redimensionar para la vista previa
            
            out.write(frame)
            #cv.imshow("Grabación", frame)
            #no subi los ultimos cambios y no me acuerdo que queria cambiar xd
            if cv.waitKey(1) == ord("q"):
                break
    finally:
        out.release()
        cv.destroyAllWindows()
        with lock:
            paro = False