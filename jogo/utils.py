import shelve


def salvar_jogo(nome_do_objeto, objeto, nome_do_arquivo):
    save = shelve.open("save.pkl")
    save[nome_do_objeto] = objeto


def carregar_jogo(nome_do_objeto, nome_do_arquivo):
    save = shelve.open("save.pkl")
    return save[nome_do_objeto]


def chunk(lista, numero):
    return [lista[x : x + numero] for x in range(0, len(lista), numero)]


class Substantivo:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return "a" if self.nome.endswith("a") else "o"


def requisitar_level(lista: list, valor: int):
    minimo = float("inf")
    lista = list(lista)
    if valor == 0:
        return lista[0]
    for valor2 in lista:
        if valor2 < valor:
            minimo = valor2
        else:
            break
    return minimo
