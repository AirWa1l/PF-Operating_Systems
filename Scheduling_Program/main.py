import sys
from Models.UserSession import UserSession
import cmd
import subprocess
from Style.transform_list import transform_list,show_executions_graphic,show_profile
from Algorithms.planificador import planificador_run

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

        if not self.us.is_authenticated():
            print("Not loggin")

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

    def do_pro(self,arg):

        if not self.us.is_authenticated():
            print("Not loggin")

        if len(arg) > 1:
            print("Use: pro")
        
        response = self.us.see_profile()

        if not response:
            print("Error showing the profile")
            return
        else:
            dic = dict(response)

            name = dic["Nickname"]
            email = dic["Email"]

            show_profile(username = name, email = email)
        
    def do_edit(self,arg):

        if not self.us.is_authenticated():
            print("Not loggin")

        args = arg.split() # name <name> email <> password <>

        name = "default"

        email = "default"

        password = "default"

        for argument in range(0,len(args)):
        
            try :

                if args[argument] == "name":
                    
                    name = args[argument + 1]

                if args[argument] == "email":

                    email = args[argument + 1]
                
                if args[argument] == "password":

                    password = args[argument + 1]

            except IndexError as e:
                
                print("Error: ",e)
                return
            

        response = self.us.update_profile(username = name,email = email, password = password)

        if response == 200:

            print("Sucefully update")
            return
        
        else:

            print("Failed update")
            return
    
    def do_rept(self,arg):

        if not self.us.is_authenticated():
            print("Not loggin")

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
        if not self.us.is_authenticated():
            print("Not loggin")
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

        except FileNotFoundError:
            print(f"Archivo no encontrado: {filename}")
        except Exception as e:
            print(f"Error al ejecutar el comando de scheduling: {e}")


    def do_exit(self, args):
        """Exit the application."""
        print("Exiting the application.")
        return True
    
    def do_gete(self,args):
        if not self.us.is_authenticated():
            print("Not loggin")

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

    