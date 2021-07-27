def chunk(lista, numero):
    return [lista[x:x + numero] for x in range(0, len(lista), numero)]
