# Models/Ejecutar.py
from tkinter import *
import sys
import os
from tkinter import messagebox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from Scheduling_Program.Algorithms.planificador import planificador_run
from Scheduling_Program.Models.UserSession import UserSession

class Ejecutar:
    def __init__(self, ventana, gui,us_service:UserSession):
        self.ventana = ventana
        self.gui = gui
        #self.top = Toplevel(self.ventana)
        #self.top.title("Ejecutar Comandos")
        self.us = us_service

        self.frame = Frame(self.ventana, borderwidth=3)
        #self.frame.pack(expand=True, fill="both")

        self.label = Label(self.frame, text="Command - Turnaround Time - Response Time", font=("Times New Roman", 14), fg="black")
        self.label.pack(pady=5)

        self.text_frame = Frame(self.frame)
        self.text_frame.pack(expand=True, fill="both")

        self.text = Text(self.text_frame, wrap="none")
        self.text.pack(side=LEFT, expand=True, fill="both")

        self.scrollbar_y = Scrollbar(self.text_frame, orient="vertical", command=self.text.yview)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)
        self.text.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = Scrollbar(self.frame, orient="horizontal", command=self.text.xview)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)
        self.text.configure(xscrollcommand=self.scrollbar_x.set)

        self.boton_cerrar = Button(self.frame, text="Cerrar", command=self.volver_a_comandos, width=10, height=1, bg="red")
        self.boton_cerrar.place(x = 240, y = 350) # pady=5

        self.actualizar_texto_comandos()
    

    def mostrar_exec_hechas(self,commands,response):
        self.text.delete(1.0,END)
        for i in range(0,len(response["turnaround times"])):

            self.text.insert(END, f" Comando : {commands[i][0]} - TAT : {response['turnaround times'][i]} - RT : {response['response times'][i]}\n")

        self.text.insert(END,f"ATAT : {response['average turnaround times']} - ART : {response['average response times']}")
    
    def show(self):
        self.gui.home.hide()
        self.frame.pack(expand=True, fill="both")
    
    def generar_resultados(self,commands,alg):

        self.text.delete(1.0,END)

        if not self.us.is_authenticated():
            messagebox.showerror("Autenticación fallida","Correo o contraseña no validos")
        else:
            dic = self.us.set_execution(commands,alg = alg)

            response = planificador_run(commands = commands,images = dic,algoritmo = alg) 

            for i in range(0,len(response["turnaround times"])):

                self.text.insert(END, f" Comando : {commands[i][0]} - TAT : {response['turnaround times'][i]} - RT : {response['response times'][i]}\n")
                
            self.text.insert(END,f"ATAT : {response['average turnaround times']} - ART : {response['average response times']}")
    
    def hide(self):
        self.frame.pack_forget()

    
    def volver_a_comandos(self):
        self.hide()
        self.gui.historial.show()
    
    def actualizar_texto_comandos(self):
        self.text.delete(1.0, END)
        for comando in self.gui.comandos_lista:
            # Simular tiempos de turnaround y respuesta para propósitos de demostración
            turnaround_time = int(comando["tiempo_inicio"]) + int(comando["tiempo_estimado"]) + 5  # Solo para ejemplo
            response_time = int(comando["tiempo_inicio"]) + 5  # Solo para ejemplo
            self.text.insert(END, f"{comando['comando']} - {turnaround_time} - {response_time}\n")
