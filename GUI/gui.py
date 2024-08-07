from tkinter import *
from Models.Home import Home
from Models.Login import Login
from Models.Register import Register
from Models.Historial import Historial
from Models.Comandos import Comandos
from Models.Ejecutar import Ejecutar
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

from Scheduling_Program.Models.UserSession import UserSession


class GUI:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("AppSO")
        self.ventana.geometry("600x400")
        self.us = UserSession()
        
        self.usuario_registrado = False
        self.comandos_lista = []
        
        self.register = None
        self.login = None
        self.historial = None
        self.comandos = None
        self.home = None
        
        self.initialize_components()
        
        self.center_window(600, 400)
        
        self.home.show()
        
    def initialize_components(self):
        self.home = Home(self.ventana, self,us_service = self.us)
        self.ejecutar = Ejecutar(self.ventana,self,us_service = self.us)
        self.register = Register(self.ventana, self,us_service = self.us)
        #self.login = Login(self.ventana, self,us_service = self.us)
        self.comandos = Comandos(self.ventana, self,us_service = self.us,ejecutar = self.ejecutar)
        self.historial = Historial(self.ventana, self,us_service = self.us, ejecutar = self.ejecutar)

        #self.ejecutar.hide()
        
    def center_window(self, width, height):
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')
        
    def run(self):
        self.ventana.mainloop()

    def agregar_comando(self, tipo_algoritmo, idp, comando, tiempo_inicio, tiempo_estimado):
        nuevo_comando = {
            "tipo_algoritmo": tipo_algoritmo,
            "idp": idp,
            "comando": comando,
            "tiempo_inicio": tiempo_inicio,
            "tiempo_estimado": tiempo_estimado
        }
        self.comandos_lista.append(nuevo_comando)
        self.historial.actualizar_historial_comandos()

if __name__ == "__main__":
    app = GUI()
    app.run()
