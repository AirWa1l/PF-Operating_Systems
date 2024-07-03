from tkinter import *
from tkinter import ttk

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from Scheduling_Program.Models.UserSession import UserSession

class Historial:
    def __init__(self, ventana, gui, us_service : UserSession):
        self.ventana = ventana
        self.gui = gui
        self.us = us_service
        self.frame = Frame(self.ventana, borderwidth=3)
        
        self.seleccionar_algoritmo = Label(self.frame, text="Seleccionar algoritmo", font=("Times New Roman", 14), fg="black")
        self.seleccionar_algoritmo.pack(pady=5)

        # Treeview para mostrar los comandos con sus detalles
        self.tree = ttk.Treeview(self.frame, columns=("TipoAlgoritmo", "IDP", "Comando", "TiempoInicio", "TiempoEstimado"), show='headings')
        self.tree.heading("TipoAlgoritmo", text="Tipo de Algoritmo")
        self.tree.heading("IDP", text="IDP")
        self.tree.heading("Comando", text="Comando")
        self.tree.heading("TiempoInicio", text="Tiempo de Inicio")
        self.tree.heading("TiempoEstimado", text="Tiempo Estimado")
        
        # Ajustar columnas
        for col in self.tree["columns"]:
            self.tree.column(col, width=100, anchor=CENTER)
        
        self.tree.pack(expand=True, fill="both")

        self.botonBackHistorial = Button(self.frame, text="Volver", command=self.volver_a_comandos, width=10, height=1, bg="red")
        self.botonBackHistorial.pack(pady=5)

    def show(self):
        self.gui.comandos.hide()
        self.frame.pack(expand=True, fill="both")
        self.actualizar_historial_comandos()

    def hide(self):
        self.frame.pack_forget()
    

    def actualizar_historial_comandos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        comandos_lista = dict(self.us.get_user_executions())
        current_idp = None
        #print(comandos_lista)
        for key,value in comandos_lista.items():
            print(value)
            procesos = value['Processes']
            alg = value["Algoritmh"]
            if key != current_idp:
                current_idp = key
                self.tree.insert("", "end", values=("", "", "", "", ""), tags=("line_separator",))
            for process in procesos:
                self.tree.insert("", "end", values=(
                    alg,
                    key,
                    process["Comando"],
                    process["Tiempo_inicio"],
                    process["Tiempo_estimado"]
                ))
        
        # Aplicar tags para las líneas divisoras
        self.tree.tag_configure("line_separator", background="gray")

    def volver_a_comandos(self):
        self.hide()
        self.gui.comandos.show()