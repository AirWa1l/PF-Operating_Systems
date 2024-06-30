import sys
#from contenedor import container_run
#from planificador import planificador_run
from Models.UserSession import UserSession
import cmd
import subprocess
from transform_list import transform_list,show_executions_graphic
from planificador import planificador_run

#us = UserSession()

class ConsoleApp(cmd.Cmd):
    intro = "Welcome to Scheduling 5 program console"
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.us = UserSession() 
        self.token = None  

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
            print("User logged out.")
        else:
           print("No user logged in.")
    
    def do_clean(self,args):

        args = args.split()

        if len(args) > 1:
            print("Use : clean")

        print("Are you sure to delete your executions ?")
        parameter = input("Press Y to continue, N to decline")

        if parameter.lower() == "y":

            self.us.clean()

        elif parameter.lower == "n":

            print("declined")
            return

        else:
            
            print("Unsupported option")
            return

        
        
    
    def do_rept(self,arg):

        args = arg.split()

        if len(args) < 2:
            print("use: <execution id> <algorithm>")
            return
        

        id_exec = int(args[0])
        algorithm = args[1]

        dic,commands = self.us.reused_user_executions(id_exec)

        if len(args) == 3:
            quatum = args[2]

            planificador_run(commands=commands,images=dic,algoritmo=algorithm,quantum=quatum)

        elif len(args) == 2:
            
            planificador_run(commands=commands,images=dic,algoritmo=algorithm)
    
    def do_exec(self,arg):
        try:
            args = arg.split()
            if len(args) != 2:
                print("Use: exec <archive.txt> <algoritmh>")
                return
            
            filename, algorithm = args 

            subprocess.run(f"cat {filename}", shell=True, capture_output=True, text=True)

            with open(filename, "r") as f:
                commands = [line.strip() for line in f]

            commands = transform_list(commands)

            dic = self.us.set_execution(commands,alg = algorithm)

            print(dic)

            if len(args) == 3:
                
                quantum = args[2] 

                planificador_run(commands=commands,images=dic,algoritmo=algorithm,quantum=quantum)

            elif len(args) == 2:
            
                planificador_run(commands=commands,images=dic,algoritmo=algorithm)

            """
            scheduling_command = f"scheduling {filename} {algorithm}"

            print(f"Executing: {scheduling_command}")

            result = subprocess.run(scheduling_command, shell=True, capture_output=True, text=True)

            print("Salida del comando:")
            print(result.stdout)
            if result.stderr:
                print("Errores:")
                print(result.stderr)
            """

        except FileNotFoundError:
            print(f"Archivo no encontrado: {filename}")
        #except Exception as e:
            #print(f"Error al ejecutar el comando de scheduling: {e}")


    def do_exit(self, args):
        """Exit the application."""
        print("Exiting the application.")
        return True
    
    def do_gete(self,args):
        execs = dict(self.us.get_user_executions())
        if execs == False:
            print("Error")

        for key,value in execs.items():
            show_executions_graphic(key,value)
    
    def do_shell(self, arg):
        """Execute a command on the system."""
        print("Executing a command of the system:", arg)
        try:
            output = subprocess.check_output(arg, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error executing the command: {e.output}")
    
    #def pass

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
    