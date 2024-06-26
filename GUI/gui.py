from tkinter import *
from tkinter import ttk

# Contenedor principal
ventana = Tk()
ventana.title("Inicio")
ventana.geometry("500x350")
ventana.resizable(False, False)


# Frames
inicio = Frame(ventana, borderwidth=3)
comandos = Frame(ventana, borderwidth=3)
historial = Frame(ventana, borderwidth=3)
historial_abajo = Frame(ventana, borderwidth=3)
historial_derecha = Frame(ventana,borderwidth=3)
inicio.pack(expand=True, fill="both")

# Definición de tamaño de row y columns
inicio.rowconfigure(0, minsize=30)
inicio.rowconfigure(1, minsize=50)
inicio.rowconfigure(2, minsize=10)
inicio.columnconfigure(0, minsize=30)
inicio.columnconfigure(1, minsize=50)
inicio.columnconfigure(2, minsize=50)

# Funciones
def center_window(window, width, height):
    # Obtener las dimensiones de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular las coordenadas para centrar la ventana
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    # Establecer la geometría para centrar la ventana
    window.geometry(f'{width}x{height}+{x}+{y}')

def iniciar():
    inicio.pack_forget()
    comandos.pack(expand=True, fill="both")
    ventana.update()
    print("Empezaste la aplicación")

def mostrarhistorial():
    comandos.pack_forget()
    historial.pack()
    historial_abajo.pack(side="left")
    historial_derecha.pack()
    ventana.update()
    print("Entraste al historial")

def devolverseComandos():
    historial.pack_forget()
    historial_abajo.pack_forget()
    historial_derecha.pack_forget()
    comandos.pack()
    ventana.update()
    print("Volviste a comandos")

#Centrar la ventana
center_window(ventana, 500, 350)

# Etiquetas inicio
bienvenida = Label(inicio, text="Bienvenido a la app", background="#E0FFFF", font=("Times New Roman", 16, "italic"), borderwidth=1, relief="sunken")
integrantes = Label(inicio, text="Integrantes:", font=("Times New Roman", 14), background="#F5CBA7", relief="ridge")
mensajeCambiar = Label(inicio, background="#52BE80", text="Ingresar comandos:", font=("Times New Roman", 14), relief="groove")

integrantes_list = Listbox(inicio)
nombres = ["Juan Pinto", "Calle"]
for name in nombres:
    integrantes_list.insert(END, name)

integrantes.grid(row=2, column=1)
bienvenida.grid(row=0, column=2, columnspan=1, sticky="e")
mensajeCambiar.grid(row=4, column=3)
integrantes_list.grid(row=3, column=1, sticky="n")

# Etiquetas comando
comando = Label(comandos, text="Comandos")
comando.grid(row=0, column=0)

# Etiquetas historial
etiquetaHistorial = Label(historial, text="Historial", relief="sunken", background="#82E0AA", padx=20, pady=10)
etiquetap02 = Label(historial, padx=60)
etiqueta04 = Label(historial,padx=70)

etiquetap02.grid(row=0, column=2)
etiqueta04.grid(row=0,column=4)
etiquetaHistorial.grid(row=0, column=3)

#Etiquetas historial_abajo

#Etiquetas historial_derecha
Lelige = Label(historial_derecha, text="Seleccionar tipo de algoritmo", relief="raised", padx=20, pady=10, font=("Arial", 12, "bold"), bg="#AED6F1", fg="#2C3E50")
Lelige.pack()

# Separadores
separador_horizontal = ttk.Separator(historial, orient="horizontal")
separador_horizontal.grid(row=1, column=0, columnspan=6, sticky="ew")

separador_vertical = ttk.Separator(historial, orient="vertical")
separador_vertical.grid(row=0, column=1, rowspan=1, sticky="ns")



# Botones
botonStart = Button(inicio, text="Start", command=iniciar, padx=20)
botonHistorial = Button(comandos, text="Historial", command=mostrarhistorial, padx=20)
botonBackHistorial = Button(historial, text='Back', command=devolverseComandos, padx=20, background="#82E0AA")


botonStart.grid(row=5, column=3, sticky="se")
botonHistorial.grid(row=1, column=1)
botonBackHistorial.grid(row=0, column=0)


#Botones historial_abajo
Bprimero = Button(historial_abajo,padx=40,pady=5)
Bsegundo = Button(historial_abajo,padx=40,pady=5)
Btercero = Button(historial_abajo,padx=40,pady=5)
Bcuarto = Button(historial_abajo,padx=40,pady=5)

Bprimero.pack()
Bsegundo.pack()
Btercero.pack()
Bcuarto.pack()

ventana.mainloop()

