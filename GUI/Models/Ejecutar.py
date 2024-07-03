# Models/Ejecutar.py
from tkinter import *

class Ejecutar:
    def __init__(self, ventana, gui):
        self.ventana = ventana
        self.gui = gui
        self.top = Toplevel(self.ventana)
        self.top.title("Ejecutar Comandos")

        self.frame = Frame(self.top, borderwidth=3)
        self.frame.pack(expand=True, fill="both")

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

        self.boton_cerrar = Button(self.frame, text="Cerrar", command=self.top.destroy, width=10, height=1, bg="red")
        self.boton_cerrar.pack(pady=5)

        self.actualizar_texto_comandos()

    def actualizar_texto_comandos(self):
        self.text.delete(1.0, END)
        for comando in self.gui.comandos_lista:
            # Simular tiempos de turnaround y respuesta para propósitos de demostración
            turnaround_time = int(comando["tiempo_inicio"]) + int(comando["tiempo_estimado"]) + 5  # Solo para ejemplo
            response_time = int(comando["tiempo_inicio"]) + 5  # Solo para ejemplo
            self.text.insert(END, f"{comando['comando']} - {turnaround_time} - {response_time}\n")
