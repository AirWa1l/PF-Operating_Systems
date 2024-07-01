from tkinter import Frame, Tk, Label, StringVar, CENTER, END, Entry, Button, Listbox
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from Scheduling_Program.Models.UserSession import UserSession


class home(Frame):
    
    def __init__(self,window,borderwith,us:UserSession):

        super().__init__(window,borderwith,relief='solid')

        self.window = window

        self.borderwith = borderwith
        
        self.us = us

        self.pack(expand = True,fill = 'both')

        self.generate_widgets()
    
    def generate_widgets(self):

        bienvenida = Label(self, text="Bienvenido a la app", font=("Times New Roman", 18), fg="red")
        integrantes = Label(self, text="Developers", font=("Times New Roman", 14), fg="black")

        nombres = ["Juan Pinto", "Juan Calle", "Adrian marin", "Francesco", "Juan Mafla"]
        integrantes_list = Listbox(self, width=15, height=len(nombres), font=("Arial", 12), justify=CENTER)

        for name in nombres:
            espacios = (30 - len(nombres)) // 2
            elemento_centralizado = f"{' ' * espacios}{nombres}"
            integrantes_list.insert(END, name)

        bienvenida.config()
        bienvenida.place(x=150,y=0)
        integrantes.place(x=40,y=70)
        integrantes_list.place(x=15,y=100)

        # Ingresar datos de usuario en el frame inicio
        username_label = Label(self, text="Usuario", bg="white")
        username_label.place(x=320, y=60)

        correo_label = Label(self, text="Correo", bg= "white")
        correo_label.place(x=325, y=120)

        password_label = Label(self, text="Contraseña", bg="white")
        password_label.place(x=310, y=180)

        username = StringVar()
        correo = StringVar()
        password = StringVar()

        username_entry = Entry(self, textvariable=username, width=20)
        correo_entry = Entry(self, textvariable=correo, width=20)
        password_entry = Entry(self, textvariable=password, width=20, show="*")

        username_entry.place(x=280, y=90)
        correo_entry.place(x=280, y=150)
        password_entry.place(x=280, y=210)

        """
        # Botones en el frame 'inicio'
        registrar = Button(self, text="Registrar", font=("Times New Roman", 14), relief="groove", command=abrir_registro, width=15, height=1)
        registrar.place(x=270, y=260)

        iniciar_sesion_btn = Button(self, text="Iniciar sesion", font=("Times New Roman", 14), relief="groove", command=iniciar_sesion, width=15, height=1)
        iniciar_sesion_btn.place(x=270, y=300)

        # Botones en el frame 'comandos'
        bot_fram_ad = Frame(comandos)
        bot_fram_ad.pack(expand=True)

        botonHistorial = Button(bot_fram_ad, text="Historial", command=mostrarhistorial, width=15, height=2, bg="orange")
        botonHistorial.pack(pady=5)

        ingrCommandos = Button(bot_fram_ad, text="Ingresar comandos", command=abrir_ingresar_comando, width=15, height=2, bg="dark salmon")
        ingrCommandos.pack(pady=5)

        logout_btn = Button(bot_fram_ad, text="Log Out", command=logout, width=15, height=2, bg="red")
        logout_btn.pack(pady=5)

        # Botón en el frame 'historial'
        botonBackHistorial = Button(historial, text="Volver", command=devolverseComandos, width=10, height=2, bg="red")
        botonBackHistorial.place(x=210,y=0)
        """
    
    def register(self):

        self.pack_forget()
        # registro_frame configuration

        #######################

        main_tittle = Label()



    
    def loggin(self):
        pass



Prove = Tk()

Prove.title("proves")
Prove.geometry("500x400")

us  = UserSession()

oka = home(Prove,3,us)
        

Prove.mainloop()
