import grabador_aux
import tkinter as tk
from tkinter import Listbox, OptionMenu
from threading import Thread
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
from tkinter import *

def iniciar_grabacion():
    nombre_archivo = Nombre_text.get() or "Grabado archivo.avi"
    # Ejecutar en un hilo separado para no bloquear la GUI
    
    #selected_index = lista_resoluciones.curselection()[0] if lista_resoluciones.curselection() else 0
    #print("Archivo"+nombre_archivo + " resolucion index" + selected_index.__str__()+ " resolucion y tipo " + str(resoluciones[selected_index]) + str(type(resoluciones[selected_index])))
    print("Archivo"+nombre_archivo + " resolucion y tipo " + str(resolucion["menu"].index(tk.StringVar(value=resolucion.cget("text")).get())) + str(type(resoluciones[resolucion["menu"].index(tk.StringVar(value=resolucion.cget("text")).get())])))
    Thread(target=grabador_aux.grabador, 
           kwargs={'resolucion':  #resoluciones[selected_index],
                    resoluciones[resolucion["menu"].index(tk.StringVar(value=resolucion.cget("text")).get())], 
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
Nombre_text = tk.Entry(ventana, width=30)
Nombre_text.insert(0, "Grabado archivo.avi")

#Resolución y fps

resoluciones=[(1920, 1080),(1366, 768),(1280, 720),(1024, 768),(800, 600)]
resolucion= OptionMenu(ventana, tk.StringVar(value="1920x1080"), *["{}x{}".format(w,h) for w,h in resoluciones])
resolucion.config(width=15)

#lista_resoluciones = Listbox(ventana, width=15, height=5)

#for w,h in resoluciones:
#    lista_resoluciones.insert(tk.END, "{}x{}".format(w,h))
#lista_resoluciones.pack()
#lista_resoluciones.selection_set(0)

# Área de visualización (ahora mostrará la vista previa)
Area = tk.Label(ventana, bg='black')

# Botones
button_frame = tk.Frame(ventana)
B_Grabar = tk.Button(button_frame, text="Grabar", padx=20, pady=10, command=iniciar_grabacion)
B_Detener = tk.Button(button_frame, text="Detener", padx=20, pady=10, command=grabador_aux.detener)

# Layout
Nombre.grid(row=2, column=0, padx=10, pady=10, sticky='w')
Nombre_text.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
button_frame.grid(row=2, column=3, padx=10, pady=10)
resolucion.grid(row=2, column=2, padx=5, pady=10, sticky='ew')
#lista_resoluciones.grid(row=2, column=2, padx=5, pady=10, sticky='ew')
B_Grabar.pack(side='left', padx=5)
B_Detener.pack(side='left', padx=5)
Area.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

# Configurar el redimensionamiento
ventana.grid_columnconfigure(1, weight=1)
ventana.grid_rowconfigure(1, weight=1)

ventana.mainloop()