from tkinter import *

class Register:
    def __init__(self, ventana, gui):
        self.ventana = ventana
        self.gui = gui
        self.frame = Frame(self.ventana, borderwidth=3)
        
        self.main_title = Label(self.frame, text="Registro base de comandos", font=("Times New Roman", 15), bg="gray26", fg="Black", width=60, height=2)
        self.main_title.pack()

        self.username_label_reg = Label(self.frame, text="Usuario", bg="white")
        self.username_label_reg.place(x=50, y=100)
        self.correo_label_reg = Label(self.frame, text="Correo", bg="white")
        self.correo_label_reg.place(x=50, y=150)
        self.password_label_reg = Label(self.frame, text="Contraseña", bg="white")
        self.password_label_reg.place(x=50, y=200)
        
        self.username_reg = StringVar()
        self.password_reg = StringVar()
        self.correo_reg = StringVar()

        self.username_entry_reg = Entry(self.frame, textvariable=self.username_reg, width=20)
        self.correo_entry_reg = Entry(self.frame, textvariable=self.correo_reg, width=20)
        self.password_entry_reg = Entry(self.frame, textvariable=self.password_reg, width=20, show="*")

        self.username_entry_reg.place(x=150, y=100)
        self.correo_entry_reg.place(x=150, y=150)
        self.password_entry_reg.place(x=150, y=200)

        self.registrar_btn = Button(self.frame, text="Registrar", command=self.guardar_usuario, width=8, height=2, bg="green")
        self.registrar_btn.place(x=150, y=250)

        self.cancelar_btn = Button(self.frame, text="Cancelar", command=self.volver_sin_mas, width=8, height=2, bg="red")
        self.cancelar_btn.place(x=250, y=250)

    def show(self):
        self.gui.home.hide()
        self.frame.pack(expand=True, fill="both")

    def hide(self):
        self.frame.pack_forget()

    def guardar_usuario(self):
        username_data = self.username_reg.get()
        password_data = self.password_reg.get()

        with open("Usuarios.txt", "w") as newfile:
            newfile.write(username_data + "\n")
            newfile.write(password_data + "\n")
        print(username_data, "\t", password_data)

        self.hide()
        self.gui.home.show()

    def volver_sin_mas(self):
        self.hide()
        self.gui.home.show()