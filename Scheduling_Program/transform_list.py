def transform_list(lista):
    nueva_lista = []
    for item in lista:
        partes = item.split(',')
        comando = partes[0]
        num1 = int(partes[1])
        num2 = int(partes[2])
        nueva_lista.append((comando, num1, num2))
    return nueva_lista

