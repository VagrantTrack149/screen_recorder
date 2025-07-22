import cv2 as cv
import numpy as np
import pyautogui
resolution=(1440,900)
codec= cv.VideoWriter_fourcc(*"XVID")
archivo_nombre="Grabado archivo.avi"
fps=60.0

out=cv.VideoWriter(archivo_nombre,codec,fps,resolution)
cv.namedWindow("Grabación",cv.WINDOW_NORMAL)
cv.resizeWindow("Grabación",480,270)

while True:
    img=pyautogui.screenshot()
    frame=np.array(img)
    frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    out.write(frame)
    cv.imshow("Grabación",frame)

    if cv.waitKey(1)==ord("q"):
        break

out.release()
cv.destroyAllWindows()