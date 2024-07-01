from tkinter import *

class Historial:
    def __init__(self, ventana, gui):
        self.ventana = ventana
        self.gui = gui
        self.frame = Frame(self.ventana, borderwidth=3)
        
        self.seleccionar_algoritmo = Label(self.frame, text="Seleccionar algoritmo", font=("Times New Roman", 14), fg="black")
        self.seleccionar_algoritmo.place(x=260,y=100)

        self.historial_Listbox = Listbox(self.frame)
        self.historial_Listbox.place(x=20, y=70)

        self.botonBackHistorial = Button(self.frame, text="Volver", command=self.volver_a_comandos, width=10, height=2, bg="red")
        self.botonBackHistorial.place(x=210,y=0)

    def show(self):
        self.gui.comandos.hide()
        self.frame.pack(expand=True, fill="both")
        self.actualizar_historial_comandos()

    def hide(self):
        self.frame.pack_forget()

    def actualizar_historial_comandos(self):
        self.historial_Listbox.delete(0, END)
        for comando in self.gui.comandos_lista:
            self.historial_Listbox.insert(END, comando)

    def volver_a_comandos(self):
        self.hide()
        self.gui.comandos.show()