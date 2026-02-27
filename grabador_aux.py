import cv2 as cv
import numpy as np
import pyautogui
from threading import Lock
from PIL import Image, ImageTk
import time
import threading

# Variables de control con protección de hilos
paro = False
lock = Lock()
current_frame = None
frame_lock = Lock()
numFrames=0

def detener():
    global paro, lock
    with lock:
        paro = True

def get_current_frame():
    global current_frame, frame_lock
    with frame_lock:
        return current_frame

def _calibrate(resolucion, duration=2):
    start = time.perf_counter()
    count = 0
    while time.perf_counter() - start < duration:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        if frame.shape[1] != resolucion[0] or frame.shape[0] != resolucion[1]:
            frame = cv.resize(frame, resolucion)
        count += 1
    elapsed = time.perf_counter() - start
    return count / elapsed

def _process_frame(img, resolucion):
    frame = np.array(img)
    # pyautogui entrega la imagen en RGB; convertir a BGR para que OpenCV la
    # escriba correctamente
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    if frame.shape[1] != resolucion[0] or frame.shape[0] != resolucion[1]:
        frame = cv.resize(frame, resolucion)
    return frame


def grabador(resolucion, fps, archivo_nombre="Grabado archivo.mp4", num_workers=None):
    
    global paro, lock, current_frame, frame_lock, numFrames

    # Reiniciar el estado de paro
    with lock:
        paro = False

    print("Calibrando fps reales")
    actual_fps = _calibrate(resolucion, duration=2)
    if fps > actual_fps:
        print(f"Los FPS solicitados ({fps}) son mayores que los que tu sistema puede sostener ({actual_fps:.2f}).")
        print(f"Se ajustará automáticamente a {actual_fps:.2f} ")
        fps = actual_fps
    else:
        print(f"Los FPS solicitados ({fps}) son alcanzables. Se usará ese valor.")

    codec = cv.VideoWriter_fourcc(*'mp4v')
    print(f"Grabando en {archivo_nombre} a {resolucion[0]}x{resolucion[1]} a {fps} FPS")
    out = cv.VideoWriter(archivo_nombre, codec, fps, resolucion)
    if not out.isOpened():
        print("ERROR")
        return

    # configuramos el tamaño del pool de hilos
    if num_workers is None:
        import multiprocessing
        num_workers = multiprocessing.cpu_count()

    from concurrent.futures import ThreadPoolExecutor, as_completed
    from collections import deque

    try:
        start_time = time.perf_counter()
        frame_count = 0
        fps_report_time = start_time
        fps_report_count = 0

        # cola para pendientes
        pending = deque()
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            while True:
                with lock:
                    if paro:
                        break

                # disparo capturas
                img = pyautogui.screenshot()
                numFrames += 1
                future = executor.submit(_process_frame, img, resolucion)
                pending.append(future)

                # reescribimos la espera
                if pending and pending[0].done():
                    frame = pending.popleft().result()

                    # vista previa
                    with frame_lock:
                        current_frame = cv.resize(frame, (640, 360))
                    out.write(frame)

                    frame_count += 1
                    elapsed = time.perf_counter() - start_time
                    expected = frame_count / fps
                    sleep_time = expected - elapsed
                    if sleep_time > 0:
                        time.sleep(sleep_time)

                # reportar fps real cada segundo
                now = time.perf_counter()
                if now - fps_report_time >= 1.0:
                    real_fps = (frame_count - fps_report_count) / (now - fps_report_time)
                    print(f"FPS reales: {real_fps:.2f} (objetivo: {fps})")
                    fps_report_time = now
                    fps_report_count = frame_count

                if cv.waitKey(1) == ord("q"):
                    break

            # vaciar los pendientes restantes
            while pending:
                frame = pending.popleft().result()
                out.write(frame)
    finally:
        out.release()
        cv.destroyAllWindows()
        with lock:
            paro = False