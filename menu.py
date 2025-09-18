import grabador_aux
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv

def iniciar_grabacion():
    nombre_archivo = Nombre_text.get() or "Grabado archivo.avi"
    # Ejecutar en un hilo separado para no bloquear la GUI
    Thread(target=grabador_aux.grabador, 
           kwargs={'resolucion': (1920, 1080), 
                   'fps': 60.0, 
                   'archivo_nombre': nombre_archivo}, 
           daemon=True).start()
    update_preview()

def update_preview():
    frame = grabador_aux.get_current_frame()
    if frame is not None:
        # Convertir el frame de OpenCV a formato compatible con Tkinter
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Actualizar el label
        Area.imgtk = imgtk  # Mantener una referencia
        Area.config(image=imgtk)
    
    # Actualzación 60fps vista previa
    ventana.after(17, update_preview)  # ≈60 FPS (1000ms/60 ≈ 16.666ms)

ventana = tk.Tk()
ventana.title("Grabador")
ventana.geometry("800x500")

# Nombre archivo
Nombre = tk.Label(ventana, text="Nombre del archivo:")
Nombre_text = tk.Entry(ventana, width=60)
Nombre_text.insert(0, "Grabado archivo.avi")

#Resolución y fps
resulocion= tk.Combobox(
    state="readonly",
    values=["(1920, 1080)", "(1366, 768)", "(1280, 720)", "(1024, 768)", "(800, 600)"]
)
resulocion.current(0)

# Área de visualización (ahora mostrará la vista previa)
Area = tk.Label(ventana, bg='black')

# Botones
button_frame = tk.Frame(ventana)
B_Grabar = tk.Button(button_frame, text="Grabar", padx=20, pady=10, command=iniciar_grabacion)
B_Detener = tk.Button(button_frame, text="Detener", padx=20, pady=10, command=grabador_aux.detener)

# Layout
Nombre.grid(row=2, column=0, padx=10, pady=10, sticky='w')
Nombre_text.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
button_frame.grid(row=2, column=2, padx=10, pady=10)
resulocion.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
B_Grabar.pack(side='left', padx=5)
B_Detener.pack(side='left', padx=5)
Area.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# Configurar el redimensionamiento
ventana.grid_columnconfigure(1, weight=1)
ventana.grid_rowconfigure(1, weight=1)

ventana.mainloop()