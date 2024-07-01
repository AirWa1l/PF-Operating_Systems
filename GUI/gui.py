from tkinter import *
from Models.Home import Home
from Models.Login import Login
from Models.Register import Register
from Models.Historial import Historial
from Models.Comandos import Comandos

class GUI:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("AppSO")
        self.ventana.geometry("500x400")
        
        self.usuario_registrado = False
        self.comandos_lista = []
        
        self.register = None
        self.login = None
        self.historial = None
        self.comandos = None
        self.home = None
        
        self.initialize_components()
        
        self.center_window(500, 400)
        
        self.home.show()
        
    def initialize_components(self):
        self.home = Home(self.ventana, self)
        self.register = Register(self.ventana, self)
        self.login = Login(self.ventana, self)
        self.comandos = Comandos(self.ventana, self)
        self.historial = Historial(self.ventana, self)
        
    def center_window(self, width, height):
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')
        
    def run(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = GUI()
    app.run()