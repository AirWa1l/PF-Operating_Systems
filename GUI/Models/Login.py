from tkinter import *
from tkinter import messagebox

class Login:
    def __init__(self, ventana, gui):
        self.ventana = ventana
        self.gui = gui
        self.frame = Frame(self.ventana, borderwidth=3)
        
        self.username_label = Label(self.frame, text="Usuario", bg="white")
        self.username_label.place(x=320, y=60)

        self.correo_label = Label(self.frame, text="Correo", bg="white")
        self.correo_label.place(x=325, y=120)

        self.password_label = Label(self.frame, text="Contraseña", bg="white")
        self.password_label.place(x=310, y=180)

        self.username = StringVar()
        self.correo = StringVar()
        self.password = StringVar()

        self.username_entry = Entry(self.frame, textvariable=self.username, width=20)
        self.correo_entry = Entry(self.frame, textvariable=self.correo, width=20)
        self.password_entry = Entry(self.frame, textvariable=self.password, width=20, show="*")

        self.username_entry.place(x=280, y=90)
        self.correo_entry.place(x=280, y=150)
        self.password_entry.place(x=280, y=210)

        self.iniciar_sesion_btn = Button(self.frame, text="Iniciar sesion", command=self.iniciar_sesion, width=15, height=2)
        self.iniciar_sesion_btn.place(x=270, y=260)

    def show(self):
        self.gui.home.hide()
        self.frame.pack(expand=True, fill="both")

    def hide(self):
        self.frame.pack_forget()

    def iniciar_sesion(self):
        username_data = self.username.get()
        password_data = self.password.get()

        try:
            with open("Usuarios.txt", "r") as file:
                stored_username = file.readline().strip()
                stored_password = file.readline().strip()
                if username_data == stored_username and password_data == stored_password:
                    self.gui.usuario_registrado = True
                    messagebox.showinfo("Inicio de sesión exitoso", "Has iniciado sesión correctamente.")
                    self.hide()
                    self.gui.comandos.show()
                else:
                    messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos.")
        except FileNotFoundError:
            messagebox.showerror("Error de inicio de sesión", "No hay usuarios registrados. Por favor, registre un usuario primero.")