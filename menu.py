import grabador_aux
import tkinter as tk
from tkinter import Listbox, OptionMenu, Spinbox, StringVar
from threading import Thread
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
import os

def update_preview():
    frame = grabador_aux.get_current_frame()
    if frame is not None:
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        Area.imgtk = imgtk  # mantener referencia
        Area.config(image=imgtk)
    
    #vista previa
    ventana.after(33, update_preview)  # 30 FPS (1000ms/30 ≈ 33ms)


def iniciar_grabacion():
    nombre_archivo = Nombre_text.get() or "Grabado archivo.mp4"
    # Ejecutar en un hilo separado para no bloquear la GUI
    #luego cambiar a ejecutar con más hilos
    
    #selected_index = lista_resoluciones.curselection()[0] if lista_resoluciones.curselection() else 0
    #print("Archivo"+nombre_archivo + " resolucion index" + selected_index.__str__()+ " resolucion y tipo " + str(resoluciones[selected_index]) + str(type(resoluciones[selected_index])))
    
    # Obtener la resolución seleccionada del OptionMenu
    # selected_resolution_str = tk.StringVar(value=resolucion.cget("text")).get()
    selected_resolution_str = resolucion_var.get()
    width_str, height_str = selected_resolution_str.split('x')
    selected_resolution = (int(width_str), int(height_str))

    # Obtener fps seleccionado (nuevo)
    selected_fps = float(fps_var.get())

    # número de trabajadores (threads) para procesar los frames
    selected_workers = int(workers_var.get())

    print(f"Iniciando grabación con resolución: {selected_resolution}, FPS: {selected_fps}, workers: {selected_workers}")

    Thread(target=grabador_aux.grabador, 
           kwargs={'resolucion': selected_resolution,
                   'fps': selected_fps,   # antes era 30.0 fijo
                   'archivo_nombre': nombre_archivo,
                   'num_workers': selected_workers}, 
           daemon=True).start()
    update_preview()

ventana = tk.Tk()
ventana.title("Grabador")
ventana.geometry("1024x768")

# Nombre archivo
Nombre = tk.Label(ventana, text="Nombre del archivo:",)
Nombre_text = tk.Entry(ventana, width=30)
Nombre_text.insert(0, "Grabacion.mp4")

#Resolución y fps

resoluciones=[(1920, 1080),(1366, 768),(1280, 720),(1024, 768),(800, 600)]
# Cambiamos a usar StringVar para poder leer el valor fácilmente
resolucion_var = StringVar(value="1920x1080")
resolucion = OptionMenu(ventana, resolucion_var, *["{}x{}".format(w,h) for w,h in resoluciones])
resolucion.config(width=15)

#selector de FPS
fps_var = StringVar(value="30")
fps_spin = Spinbox(ventana, from_=1, to=120, increment=1, textvariable=fps_var, width=10)
fps_label = tk.Label(ventana, text="FPS:")

# selector de núcleos/trabajadores
workers_var = StringVar(value=str(os.cpu_count()))
workers_label = tk.Label(ventana, text="Hilos:")
workers_spin = Spinbox(ventana, from_=1, to=64, increment=1, textvariable=workers_var, width=5)

#lista_resoluciones = Listbox(ventana, width=15, height=5)

#for w,h in resoluciones:
#    lista_resoluciones.insert(tk.END, "{}x{}".format(w,h))
#lista_resoluciones.pack()
#lista_resoluciones.selection_set(0)

# Área de vista previa
Area = tk.Label(ventana, bg='black')

# Botones
button_frame = tk.Frame(ventana)
B_Grabar = tk.Button(button_frame, text="Grabar", padx=20, pady=10, command=iniciar_grabacion)
B_Detener = tk.Button(button_frame, text="Detener", padx=20, pady=10, command=grabador_aux.detener)

# Layout
Nombre.grid(row=2, column=0, columnspan=1,padx=10, pady=10, sticky='w')
Nombre_text.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
fps_label.grid(row=2, column=2, padx=(10,0), pady=10, sticky='e')
fps_spin.grid(row=2, column=3, padx=(0,10), pady=10, sticky='w')
workers_label.grid(row=2, column=4, padx=(10,0), pady=10, sticky='e')
workers_spin.grid(row=2, column=5, padx=(0,10), pady=10, sticky='w')
resolucion.grid(row=2, column=6, padx=10, pady=10, sticky='ew')
button_frame.grid(row=2, column=7, padx=10, pady=10)
#lista_resoluciones.grid(row=2, column=2, padx=5, pady=10, sticky='ew')
B_Grabar.pack(side='left', padx=5)
B_Detener.pack(side='left', padx=5)
Area.grid(row=1, column=0, columnspan=10, padx=10, pady=10, sticky='nsew')

# Configurar el redimensionamiento
ventana.grid_columnconfigure(1, weight=1)
ventana.grid_rowconfigure(1, weight=1)

ventana.mainloop()