import grabador_aux
import tkinter as tk
from threading import Thread

def iniciar_grabacion():
    nombre_archivo=Nombre_text.get()+".avi" or "Grabado archivo.avi"
    Thread(target=grabador_aux.grabador,
           kwargs={'resolucion':(1920,1080), 'fps':60.0, 'archivo_nombre':nombre_archivo}).start()

ventana=tk.Tk()
ventana.title("Grabador")
ventana.geometry("600x400")
#Nombre archivo
Nombre=tk.Label(ventana,text="Nombre del archivo")
Nombre_text=tk.Entry(ventana,width=60)
#Grabación
Area=tk.Label(ventana,height=17, width=50, bg='lightgray')
#boton grabar
B_Grabar=tk.Button(ventana,text="Grabar",padx=20,pady=10,command=iniciar_grabacion)
B_detener=tk.Button(ventana,text="Detener",padx=20,pady=10,command=grabador_aux.detener)

Area.grid(rowspan=2,columnspan=2)
Nombre.grid(row=3,column=0)
Nombre_text.grid(row=3,column=1)
B_Grabar.grid(row=3,column=2)
B_detener.grid(row=2,column=2)
ventana.mainloop()
