from colorama import Fore, Style, init

def transform_list(lista):
    nueva_lista = []
    for item in lista:
        partes = item.split(',')
        comando = partes[0]
        num1 = int(partes[1])
        num2 = int(partes[2])
        nueva_lista.append((comando, num1, num2))
    return nueva_lista

def show_executions_graphic(id_exec:str,processes : list):

    init()

    RED = Fore.RED
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL

    alg = processes["Algoritmh"]

    print("")
    print(RED + f"For execution: {id_exec}" + RESET + MAGENTA + " Algorithm : " + f"{alg}" + RESET)
    print("")

    procesos = processes["Processes"]

    #print(procesos)
    
    for process in procesos:

        comando = process["Comando"]
        ti = process["Tiempo_inicio"]
        te = process["Tiempo_estimado"]

        comando = WHITE + f"Command : {comando}" + RESET

        inicio = YELLOW + f"Init Time : {ti}" + RESET 

        estimado =  CYAN + f"Estimed Time : {te}" + RESET

        print(comando + "  " + inicio + "  " + estimado)

        print("")


