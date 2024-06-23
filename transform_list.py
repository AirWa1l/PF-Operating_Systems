def transform_list(lista):
    nueva_lista = []
    for item in lista:
        partes = item.split(',')
        comando = partes[0]
        num1 = int(partes[1])
        num2 = int(partes[2])
        nueva_lista.append((comando, num1, num2))
    return nueva_lista

class commands():

    def __init__(self,list_not_tranformed) -> None:
        self.listica_not = list_not_tranformed
        self.listica_yes = []
    
    def transform_list(self):
        nueva_lista = []
        for item in self.listica_not:
            partes = item.split(',')
            comando = partes[0]
            num1 = int(partes[1])
            num2 = int(partes[2])
            nueva_lista.append((comando, num1, num2))
        self.listica_yes = nueva_lista

    def get_listica_yes(self):
        return self.listica_yes