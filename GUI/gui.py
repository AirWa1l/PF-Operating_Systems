from tkinter import *

#Contenedor principal
ventana = Tk()
ventana.title("Inicio")
ventana.geometry("500x400")
ventana.grid_rowconfigure(0, weight=3)
ventana.grid_columnconfigure(0,weight=3)
ventana.resizable(False,False)
ventana.iconbitmap('icono.ico')



#Frames
inicio = Frame(ventana,borderwidth=3)
comandos = Frame(ventana,borderwidth=3)

inicio.pack(expand=True, fill="both")

#definicion de tamaño de row y columns
inicio.rowconfigure(0, minsize=20)
inicio.rowconfigure(1, minsize=50)
inicio.rowconfigure(2, minsize=50)
inicio.columnconfigure(0, minsize=50)
inicio.columnconfigure(1, minsize=50)
inicio.columnconfigure(2, minsize=50)

#Funciones
def iniciar():
    inicio.destroy()
    comandos.pack(expand=True, fill="both")
    print("Empezaste la aplicacion")


#Etiquetas inicio
bienvenida = Label(inicio, text="Bienvenido a la app",background= "#E0FFFF",font=("Times New Roman", 16, "italic"), borderwidth=1, relief="sunken")
integrantes = Label(inicio, text= "Integrantes:")
p00 = Label(inicio)


integrantes.grid(row=4,column=4)
bienvenida.grid(row=0, column=1, columnspan=2, sticky="nsew")
p00.grid(row=0,column=0)




#etiquetas comando
comando = Label(comandos, text="Comandos")

comando.grid(row=0,column=0)

#etiquetas historial


#botones
botonStart = Button(inicio, text ="Start", command = iniciar, padx=20)
botonStart.grid(row=4,column=3)

ventana.mainloop()
