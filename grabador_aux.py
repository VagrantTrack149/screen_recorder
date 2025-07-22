import cv2 as cv
import numpy as np
import pyautogui
from threading import Lock

paro = False
lock = Lock()

def detener():
    global paro, lock
    with lock:
        paro = True

def grabador(resolucion=(1920,1080), fps=60.0, archivo_nombre="Grabado archivo.avi"):
    global paro, lock
    with lock:
        paro = False

    codec= cv.VideoWriter_fourcc(*"XVID")
    
    out=cv.VideoWriter(archivo_nombre,codec,fps,resolucion)
    try:
        while True:
            # Verificar si se debe detener
            with lock:
                if paro:
                    break
            
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            out.write(frame)
            cv.imshow("Grabación", frame)
            
            if cv.waitKey(1) == ord("q") or paro:
                break
    finally:
        out.release()
        cv.destroyAllWindows()
        with lock:
            paro = False


