import shelve


def salvar_jogo(nome_do_objeto, objeto, nome_do_arquivo):
    save = shelve.open("save.pkl")
    save[nome_do_objeto] = objeto


def carregar_jogo(nome_do_objeto, nome_do_arquivo):
    save = shelve.open("save.pkl")
    return save[nome_do_objeto]


def chunk(lista, numero):
    return [lista[x : x + numero] for x in range(0, len(lista), numero)]


class Artigo:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        # o artigo não cobre todos os casos mas cobre o suficiente para o jogo.
        if self.nome[-1] in "ao":
            return self.nome[-1]
        elif self.nome.endswith("s"):
            if self.nome[-2] in "ao":
                return self.nome[-2:]
        else:
            return "o"


def requisitar_level(lista: list, valor: int):
    """Função que retorna o lvl minimo."""
    minimo = float("inf")
    lista = list(lista)
    if valor <= lista[0]:
        return lista[0]
    for valor2 in lista:
        if valor2 < valor:
            minimo = valor2
        else:
            break
    return minimo


def regra_3(status: int, porcentagem: int, status2: int):
    """Função que retorna o resultado da regra de 3."""
    return int((status2 * porcentagem) / status)


def arrumar_porcentagem(valor: int) -> int:
    """Função que arruma o valor da porcentagem para range(0, 80)"""
    if valor > 80:
        return 80
    elif valor < 0:
        return 0
    else:
        return valor
