from tkinter import *

#Contenedor principal
ventana = Tk()
ventana.title("Inicio")
ventana.geometry("500x400")

ventana.resizable(False,False)

#ventana.iconbitmap('https://github.com/AirWa1l/PF-Operating_Systems/blob/GUI/GUI/icono.ico')



#Frames
inicio = Frame(ventana,borderwidth=3)
comandos = Frame(ventana,borderwidth=3)

inicio.pack(expand=True, fill="both")

#definicion de tamaño de row y columns
inicio.rowconfigure(0, minsize=50)
inicio.rowconfigure(1, minsize=50)
inicio.rowconfigure(2, minsize=10)
inicio.columnconfigure(0, minsize=50)
inicio.columnconfigure(1, minsize=50)
inicio.columnconfigure(2, minsize=50)

#Funciones
def iniciar():
    inicio.destroy()
    comandos.pack(expand=True, fill="both")
    ventana.update()
    print("Empezaste la aplicacion")


#Etiquetas inicio
bienvenida = Label(inicio, text="Bienvenido a la app",background= "#E0FFFF",font=("Times New Roman", 16, "italic"), borderwidth=1,relief="sunken")
integrantes = Label(inicio, text= "Integrantes:", font=("Times New Roman", 14), background="#F5CBA7",relief="ridge")
mensajeCambiar = Label(inicio, background="#52BE80" ,text="Ingresar comandos", font=("Times New Roman", 14),relief="groove")

integrantes_list = Listbox(inicio)
nombres = ["Nombre1", "nombre2"]
for name in nombres:
    integrantes_list.insert(END,name)

integrantes.grid(row=2,column=1)
bienvenida.grid(row=0, column=2, columnspan=1, sticky="e")
mensajeCambiar.grid(row=4,column=3)
integrantes_list.grid(row=3, column=1, sticky="n")


#etiquetas comando
comando = Label(comandos, text="Comandos")

comando.grid(row=0,column=0)

#etiquetas historial


#botones
botonStart = Button(inicio, text ="Start", command = iniciar, padx=20)
botonStart.grid(row=5,column=3, sticky="se", )

ventana.mainloop()
