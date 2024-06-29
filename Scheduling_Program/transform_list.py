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
    RESET = Style.RESET_ALL

    print("")
    print(RED + f"For execution: {id_exec}" + RESET)
    print("")
    for process in processes:

        comando = process["Comando"]
        ti = process["Tiempo_inicio"]
        te = process["Tiempo_estimado"]

        print(WHITE + f"Command : {comando}" + RESET)
        print("")
        print(YELLOW + f"Init Time : {ti}" + RESET )
        print("")
        print(CYAN + f"Estimed Time : {te}" + RESET)
        print("")
        print("")


