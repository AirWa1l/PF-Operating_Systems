import sys
from contenedor import container_run
from planificador import planificador_run
from Models.UserSession import UserSession
import cmd

#us = UserSession()

class ConsoleApp(cmd.Cmd):
    intro = "Welcome to Scheduling 5 program console"
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.us = UserSession()  # Instancia de la clase UserSession
        self.token = None  # Variable para almacenar el token de sesión

    def do_register(self, args):
        """Register a new user."""
        if args:
            n,nickname,e,email,p,password = args.split()
            
            if n == "name" and e == "email" and p == "password" :
                correct_registration = self.us.register(nickname,email,password)

                if not correct_registration:
                    
                    print("Registration failed")
            else:

                print("Parameters not okey, use the struct 'register name <name> email <email> password <password>'")


        else:
            print("Registration functionality is not implemented yet.")

    def do_login(self, args):
        """Log in with username and password."""
        if self.us.is_authenticated():
            print("User is already authenticated.")
        else:
            if args:
                # Puedes procesar los argumentos si es necesario
                username, password = args.split()
            else:
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
            
            if self.us.authenticate(username=username, password=password):
                #self.token = self.us.get_token()
                print("User authenticated.")

    def do_logout(self, args):
        """Log out the current user."""
        if self.us.is_authenticated():
            self.us.log_out()
            self.token = None
            #print("User logged out.")
        #else:
           #print("No user logged in.")

    def do_salir(self, args):
        """Exit the application."""
        print("Exiting the application.")
        return True

    def default(self, line):
        print(f"Command '{line}' not recognized. Type 'help' for a list of available commands.")

    def emptyline(self):
        pass

if __name__ == "__main__":

    if len(sys.argv) > 1:
        print("Start the script first")

    app = ConsoleApp()
    app.cmdloop()

    #if len(sys.argv) < 4:
        #print("Error: not enough parameters. Usage: main.py container <commands_file> planner <algorithm>")
        #sys.exit(1)



    
"""
    container = sys.argv[1]
    planner = sys.argv[3]

    if container == "container":

        commands = container_run()

    if planner == "planner":
        algorithm = sys.argv[4] if len(sys.argv) > 4 else 'fcfs'
        quantum = int(sys.argv[5]) if len(sys.argv) > 5 else 2
        planificador_run(commands=commands, ,algoritmo=algorithm, quantum=quantum)
"""

# if __name__ == "__main__":
#     print(sys.argv)
#     if 1 < len(sys.argv) < 3:
#         print("Error: not parameter digited, need to put main.py container planner")
#         sys.exit(1)
#     container = sys.argv[1]
#     planner = sys.argv[3]

#     if container == "container":

#         commands = container_run()

#     if planner == "planner":

#         planificador_run(commands=commands)
    