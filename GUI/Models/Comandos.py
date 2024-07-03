from tkinter import *

class Comandos:
    def __init__(self, ventana, gui):
        self.ventana = ventana
        self.gui = gui
        self.frame = Frame(self.ventana, borderwidth=3)
        
        self.main_frame = Frame(self.frame)
        self.comando_frame = Frame(self.frame)
        
        self.setup_main_ui()
        self.setup_comando_ui()

    def setup_main_ui(self):
        self.bot_fram_ad = Frame(self.main_frame)
        self.bot_fram_ad.pack(expand=True)

        self.botonHistorial = Button(self.bot_fram_ad, text="Historial", command=self.mostrar_historial, width=15, height=2, bg="orange")
        self.botonHistorial.pack(pady=5)

        self.ingrCommandos = Button(self.bot_fram_ad, text="Ingresar comandos", command=self.abrir_ingresar_comando, width=15, height=2, bg="dark salmon")
        self.ingrCommandos.pack(pady=5)

        self.logout_btn = Button(self.bot_fram_ad, text="Log Out", command=self.logout, width=15, height=2, bg="red")
        self.logout_btn.pack(pady=5)

    def setup_comando_ui(self):
        self.tipo_algoritmo_label = Label(self.comando_frame, text="Tipo de Algoritmo", bg="lightblue")
        self.tipo_algoritmo_label.place(x=40, y=10)
        
        self.tipo_algoritmo_entry = Entry(self.comando_frame, width=23)
        self.tipo_algoritmo_entry.place(x=10, y=40)

        comando_label = Label(self.comando_frame, text="Ingrese el comando", bg="lightblue")
        comando_label.place(x=40, y=70)
        
        self.comando_entry = Entry(self.comando_frame, width=23)
        self.comando_entry.place(x=10, y=100)

        stTime_label = Label(self.comando_frame, text="Tiempo Inicio", bg="lightblue")
        stTime_label.place(x=55, y=130)
        self.stTime_entry = Entry(self.comando_frame, width=23)
        self.stTime_entry.place(x=10, y=160)

        esTime_label = Label(self.comando_frame, text="Tiempo estimado", bg="lightblue")
        esTime_label.place(x=45, y=190)
        self.esTime_entry = Entry(self.comando_frame, width=23)
        self.esTime_entry.place(x=10, y=220)

        vcmd = (self.comando_frame.register(self.validar_entry), '%P')
        self.stTime_entry.config(validate='key', validatecommand=vcmd)
        self.esTime_entry.config(validate='key', validatecommand=vcmd)

        guardar_btn = Button(self.comando_frame, text="Guardar comando", command=self.guardar_comando, bg="green", fg="white", width=20)
        guardar_btn.place(x=10, y=260)

        self.comandos_listbox_label = Label(self.comando_frame, text="Lista de Comandos", bg="lightblue")
        self.comandos_listbox_label.place(x=290, y=10)
        self.comandos_listbox = Listbox(self.comando_frame, width=34, height=18)
        self.comandos_listbox.place(x=210, y=50)

        cerrar_btn = Button(self.comando_frame, text="Cerrar", command=self.cerrar_ingresar_comando, bg="red", fg="white", width=20)
        cerrar_btn.place(x=10, y=300)

    def show(self):
        self.frame.pack(expand=True, fill="both")
        self.main_frame.pack(expand=True, fill="both")

    def hide(self):
        self.frame.pack_forget()

    def mostrar_historial(self):
        self.hide()
        self.gui.historial.show()

    def abrir_ingresar_comando(self):
        self.main_frame.pack_forget()
        self.comando_frame.pack(expand=True, fill="both")

    def cerrar_ingresar_comando(self):
        self.comando_frame.pack_forget()
        self.main_frame.pack(expand=True, fill="both")

    def validar_entry(self, text):
        return text.isdigit() or text == ""

    def guardar_comando(self):
        tipo_algoritmo = self.tipo_algoritmo_entry.get().strip()
        comando = self.comando_entry.get().strip()
        tiempo_inicio = self.stTime_entry.get().strip()
        tiempo_estimado = self.esTime_entry.get().strip()
        
        if tipo_algoritmo and comando and tiempo_inicio and tiempo_estimado:
            nuevo_comando = {
                "tipo_algoritmo": tipo_algoritmo,
                "idp": self.generar_idp(),
                "comando": comando,
                "tiempo_inicio": tiempo_inicio,
                "tiempo_estimado": tiempo_estimado
            }
            self.gui.comandos_lista.append(nuevo_comando)
            self.tipo_algoritmo_entry.delete(0, END)
            self.comando_entry.delete(0, END)
            self.stTime_entry.delete(0, END)
            self.esTime_entry.delete(0, END)
            self.actualizar_lista_comandos()
            print(self.gui.comandos_lista)  # Para ver los comandos guardados en la consola

    def generar_idp(self):
        return len(self.gui.comandos_lista) + 1  # Simplemente incrementa el IDP basado en la cantidad de comandos

    def actualizar_lista_comandos(self):
        self.comandos_listbox.delete(0, END)
        for comando in self.gui.comandos_lista:
            self.comandos_listbox.insert(END, comando["comando"])

    def logout(self):
        self.hide()
        self.gui.home.show()
        self.gui.usuario_registrado = False


