def chunk(lista, numero):
    return [lista[x:x + numero] for x in range(0, len(lista), numero)]


class Substantivo:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return 'a' if self.nome.endswith('a') else 'o'
