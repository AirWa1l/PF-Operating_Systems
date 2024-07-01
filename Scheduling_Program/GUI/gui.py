from tkinter import *
from tkinter import messagebox

# Contenedor principal
ventana = Tk()
ventana.title("JaGUI")
ventana.geometry("500x400")  # Ajuste del tamaño de la ventana principal más pequeña

# Frames
inicio = Frame(ventana, borderwidth=3)
comandos = Frame(ventana, borderwidth=3)
historial = Frame(ventana, borderwidth=3)
historial_abajo = Frame(ventana, borderwidth=3)
historial_derecha = Frame(ventana, borderwidth=3)
inicio.pack(expand=True, fill="both")

# Definición de tamaño de row y columns
inicio.rowconfigure(0, minsize=30)
inicio.rowconfigure(1, minsize=50)
inicio.rowconfigure(2, minsize=10)
inicio.columnconfigure(0, minsize=30)
inicio.columnconfigure(1, minsize=50)
inicio.columnconfigure(2, minsize=50)

# Variables globales
usuario_registrado = False
comandos_lista = []

# Funciones
def center_window(window, width, height):
    # Obtener las dimensiones de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular las coordenadas para centrar la ventana
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    # Establecer la geometría para centrar la ventana
    window.geometry(f'{width}x{height}+{x}+{y}')

def iniciar():
    global usuario_registrado
    if usuario_registrado:
        inicio.pack_forget()
        comandos.pack(expand=True, fill="both")
        ventana.update()
        print("Empezaste la aplicación")
    else:
        messagebox.showwarning("Acceso denegado", "Debe iniciar sesión antes de continuar.")

# Abre una ventana para poder registrar el usuario
def abrir_registro():
    # Elimina todos los widgets dentro del frame 'inicio'
    for widget in inicio.winfo_children():
        widget.destroy()
    
    # Crea los nuevos widgets de registro en el frame 'inicio'
    main_title = Label(inicio, text="Registro base de comandos", font=("Times New Roman", 15), bg="gray26", fg="Black", width=60, height=2)
    main_title.pack()

    username_label_reg = Label(inicio, text="Usuario", bg="white")
    username_label_reg.place(x=50, y=100)
    correo_label_reg = Label(inicio, text="Correo", bg="white")
    correo_label_reg.place(x=50, y=150)
    password_label_reg = Label(inicio, text="Contraseña", bg="white")
    password_label_reg.place(x=50, y=200)
    
    username_reg = StringVar()
    password_reg = StringVar()
    correo_label_reg = StringVar()

    username_entry_reg = Entry(inicio, textvariable=username_reg, width=20)
    correo_entry_reg = Entry(inicio, textvariable=correo_label_reg, width=20)
    password_entry_reg = Entry(inicio, textvariable=password_reg, width=20, show="*")

    username_entry_reg.place(x=150, y=100)
    correo_entry_reg.place(x=150, y=150)
    password_entry_reg.place(x=150, y=200)
    
    # Función para guardar usuario en "Usuarios.txt"
    def guardar_usuario():
        username_data = username_reg.get()
        password_data = password_reg.get()

        with open("Usuarios.txt", "w") as newfile:
            newfile.write(username_data + "\n")
            newfile.write(password_data + "\n")

        print(username_data, "\t", password_data)

        # Reinicia el frame 'inicio' después de guardar
        inicio.pack()

    def volver_sin_mas():
        # Reinicia el frame
        inicio.pack()

    registrar_btn = Button(inicio, text="Registrar", command=guardar_usuario, width=8, height=2, bg="green")
    registrar_btn.place(x=150, y=250)

    cancelar_btn = Button(inicio, text="Cancelar", command=volver_sin_mas, width=8, height=2, bg="red")
    cancelar_btn.place(x=250, y=250)

    ventana.update()

# Abre una nueva ventana confirmando el proceso de registro
def ventana_confirmacion():
    confirmVentana = Toplevel()
    confirmVentana.geometry("400x400")
    confirmVentana.title("Confirmación de Registro")
    confirmVentana.resizable(False, False)
    confirmVentana.config(background="lightgreen")

    confirm_label = Label(confirmVentana, text="Registro Exitoso", font=("Times New Roman", 15), bg="gray26", fg="Black", width=60, height=2)
    confirm_label.pack()

# Definiremos una funcion que valide que solo lo ingresado en los campos de
# numeros como stTime y esTime sean solo valores numericos
def validar_entry(text):
    return text.isdigit() or text == ""

# Permite el inicio de los comandos y guardarlos
def abrir_ingresar_comando():
    for widget in comandos.winfo_children():
        widget.destroy()

    # comandos.configure(bg="cyan")

    comando_label = Label(comandos, text="Ingrese el comando", bg="lightblue")
    comando_label.place(x=40, y=10)
    comando_entry = Entry(comandos, width=23)
    comando_entry.place(x=10, y=40)

    stTime_label = Label(comandos, text="Tiempo Inicio", bg="lightblue")
    stTime_label.place(x=55, y=70)
    stTime_entry = Entry(comandos, width=23)
    stTime_entry.place(x=10, y=100)

    esTime_label = Label(comandos, text="Tiempo estimado", bg="lightblue")
    esTime_label.place(x=45, y=130)
    esTime_entry = Entry(comandos, width=23)
    esTime_entry.place(x=10, y=160)
    

    # Registra la funcion creada
    vcmd = (comandos.register(validar_entry), '%P')

    # Aplicamos la validacion a stTime y esTime
    stTime_entry.config(validate='key', validatecommand=vcmd)
    esTime_entry.config(validate='key', validatecommand=vcmd)

    def guardar_comando():
        comando = comando_entry.get().strip()
        if comando:
            comandos_lista.append(comando)
            comando_entry.delete(0, END)
            actualizar_lista_comandos()
            print(comandos_lista)  # Para ver los comandos guardados en la consola

    guardar_btn = Button(comandos, text="Guardar comando", command=guardar_comando, bg="green", fg="white", width=20)
    guardar_btn.place(x=10, y=305)

    comandos_listbox_label = Label(comandos, text="Lista de Comandos", bg="lightblue")
    comandos_listbox_label.place(x=290, y=10)

    comandos_listbox = Listbox(comandos, width=34, height=18)
    comandos_listbox.place(x=210, y=50)

    def actualizar_lista_comandos():
        comandos_listbox.delete(0, END)
        for comando in comandos_lista:
            comandos_listbox.insert(END, comando)

    cerrar_btn = Button(comandos, text="Cerrar", command=volver_a_comandos, bg="red", fg="white", width=20)
    cerrar_btn.place(x=10, y=345)

    ventana.update()

def volver_a_comandos():
    for widget in comandos.winfo_children():
        widget.destroy()
    # Añadir botones originales al frame "comandos"
    bot_fram_ad = Frame(comandos)
    bot_fram_ad.pack(expand=True)

    botonHistorial = Button(bot_fram_ad, text="Historial", command=mostrarhistorial, width=15, height=2, bg="orange")
    botonHistorial.pack(pady=5)

    ingrCommandos = Button(bot_fram_ad, text="Ingresar comandos", command=abrir_ingresar_comando, width=15, height=2, bg="dark salmon")
    ingrCommandos.pack(pady=5)

    logout_btn = Button(bot_fram_ad, text="Log Out", command=logout, width=15, height=2, bg="red")
    logout_btn.pack(pady=5)

    ventana.update()

# Permite el inicio de sesión si el usuario ya está registrado
def iniciar_sesion():
    global usuario_registrado
    username_data = username.get()
    password_data = password.get()

    try:
        with open("Usuarios.txt", "r") as file:
            stored_username = file.readline().strip()
            stored_password = file.readline().strip()
            if username_data == stored_username and password_data == stored_password:
                usuario_registrado = True
                messagebox.showinfo("Inicio de sesión exitoso", "Has iniciado sesión correctamente.")
                inicio.pack_forget()  # Oculta el frame de inicio
                comandos.pack(expand=True, fill="both")  # Muestra el frame de comandos
                volver_a_comandos()
                print("Empezaste la aplicación")
            else:
                messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos.")
    except FileNotFoundError:
        messagebox.showerror("Error de inicio de sesión", "No hay usuarios registrados. Por favor, registre un usuario primero.")

def logout():
    global usuario_registrado
    usuario_registrado = False
    username.set("")
    correo.set("")
    password.set("")
    comandos.pack_forget()
    inicio.pack(expand=True, fill="both")
    ventana.update()
    print("Cerraste sesión")

def mostrarhistorial():
    comandos.pack_forget()
    historial.pack()
    historial_abajo.pack(side="left")
    historial_derecha.pack()
    ventana.update()
    print("Entraste al historial")

def devolverseComandos():
    historial.pack_forget()
    historial_abajo.pack_forget()
    historial_derecha.pack_forget()
    comandos.pack()
    ventana.update()
    print("Volviste a comandos")

# Centrar la ventana
center_window(ventana, 500, 400)  # Centrar la ventana principal con las nuevas dimensiones

# Etiquetas inicio
bienvenida = Label(inicio, text="Bienvenido a la app", font=("Times New Roman", 18), fg="red")
integrantes = Label(inicio, text="Developers", font=("Times New Roman", 14), fg="black")

integrantes_list = Listbox(inicio)
nombres = ["Juan Pinto", "Calle", "Adrian marin", "Franccesco", "Mafla"]
for name in nombres:
    integrantes_list.insert(END, name)

bienvenida.grid(row=0, column=2, padx=35, pady=10, sticky="nsew")
integrantes.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
integrantes_list.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

# Ingresar datos de usuario en el frame inicio
username_label = Label(inicio, text="Usuario", bg="white")
username_label.place(x=320, y=60)

correo_label = Label(inicio, text="Correo", bg= "white")
correo_label.place(x=325, y=120)

password_label = Label(inicio, text="Contraseña", bg="white")
password_label.place(x=310, y=180)

username = StringVar()
correo = StringVar()
password = StringVar()

username_entry = Entry(inicio, textvariable=username, width=20)
correo_entry = Entry(inicio, textvariable=correo, width=20)
password_entry = Entry(inicio, textvariable=password, width=20, show="*")

username_entry.place(x=270, y=90)
correo_entry.place(x=270, y=150)
password_entry.place(x=270, y=210)

# Botones en el frame 'inicio'
registrar = Button(inicio, text="Registrar", font=("Times New Roman", 14), relief="groove", command=abrir_registro, width=15, height=1)
registrar.place(x=270, y=260)

iniciar_sesion_btn = Button(inicio, text="Iniciar sesion", font=("Times New Roman", 14), relief="groove", command=iniciar_sesion, width=15, height=1)
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
botonBackHistorial.grid(row=0, column=0)

ventana.mainloop()
