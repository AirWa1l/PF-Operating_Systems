from tkinter import *
from tkinter import ttk

class Historial:
    def __init__(self, ventana, gui):
        self.ventana = ventana
        self.gui = gui
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
        self.botonRepetirComando = Button(self.frame, text="Repetir", command=self.repetir_comando_seleccionado , width=10, height=1, bg="green")
        self.botonRepetirComando.pack(pady=5)

    def show(self):
        self.gui.comandos.hide()
        self.frame.pack(expand=True, fill="both")
        self.actualizar_historial_comandos()

    def hide(self):
        self.frame.pack_forget()

    def actualizar_historial_comandos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        current_idp = None
        for comando in self.gui.comandos_lista:
            if comando["idp"] != current_idp:
                current_idp = comando["idp"]
                self.tree.insert("", "end", values=("", "", "", "", ""), tags=("line_separator",))
            self.tree.insert("", "end", values=(
                comando["tipo_algoritmo"],
                comando["idp"],
                comando["comando"],
                comando["tiempo_inicio"],
                comando["tiempo_estimado"]
            ))
        
        # Aplicar tags para las líneas divisoras
        self.tree.tag_configure("line_separator", background="gray")

    def volver_a_comandos(self):
        self.hide()
        self.gui.comandos.show()

    def repetir_comando_seleccionado(self):
        comando_seleccionado = self.tree.selection()
        if comando_seleccionado:
            comando = self.tree.item(comando_seleccionado)
            comando_values = comando["values"]
            print(f"Repetir comando: {comando_values}")            
            # Agregar Aqui la logica para que despliegue el
            # nuevo frame :D "Aqui va la cosa, Calle y Pinto"
        else:
            self.mostrar_advertencia()

    def mostrar_advertencia(self):
        ventana_advertencia = Toplevel(self.ventana)
        ventana_advertencia.title("Advertencia")
        ventana_advertencia.geometry("300x100")
        self.mensajito = Label(ventana_advertencia, text="No se ha seleccionado ningún comando", font=("Arial", 12))
        self.mensajito.pack(expand=True)
        self.ventana.after(1000, ventana_advertencia.destroy)