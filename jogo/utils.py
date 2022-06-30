from itertools import takewhile
from statistics import mean


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


def calcular_experiencia(valor) -> list[float, int]:
    """Função que retorna uma lista com os valores dos leveis."""
    valor_minimo = (75 * valor) // 100
    media = mean([valor, valor_minimo])
    return [media * x for x in range(1, 9)]


class Contador:
    def __init__(self, contagem_maxima: int):
        self._contagem_maxima = contagem_maxima
        self._contagem = 0

    def acrescentar(self):
        self._contagem += 1

    def resetar(self):
        self._contagem = 0

    @property
    def usar(self):
        return True if self._contagem > self._contagem_maxima else False


class Acumulador:
    def __init__(self, valor: int, leveis: list, level: int = 1):
        self.valor = 0
        self._leveis = leveis
        leveis += [float("inf")]
        self._leveis_dict = dict(enumerate(leveis, 1))
        self.level = level
        self.depositar_valor(valor)

    def __repr__(self):
        return f"{self.valor}"

    def __str__(self):
        return f"{self.valor}"

    def __int__(self):
        return self.valor

    def depositar_valor(self, valor: int):
        level_maximo = list(enumerate(self._leveis, 1))[-1][0]
        if self.level > level_maximo:
            self.level = level_maximo
        valor_requerido = self._leveis_dict.get(self.level)
        self.valor += valor
        while self.valor >= valor_requerido:
            diferenca = self.valor - valor_requerido
            if diferenca >= 0:
                self.valor -= valor_requerido
                self.level += 1
            else:
                self.valor -= diferenca
            valor_requerido = self._leveis_dict.get(self.level)
        if valor_requerido == float("inf"):
            self.valor = 0

    def valor_total(self):
        valor = self._leveis_dict.get(self.level - 1)
        valores = takewhile(lambda x: x <= valor, self._leveis)
        return sum(valores) + self.valor
