from random import choice, randint

from jogo.itens.moedas import Draconica
from jogo.itens.vestes import roupas_draconicas


class Caixa:
    tipo = "Caixa"
    nome = "Caixa comum"

    def __init__(self, item):
        self.item = item
        self.consumida = False
        self.classe = "Caixa"

    def __repr__(self):
        return f"Caixa: {self.nome.capitalize()}"

    def consumir(self):
        raise NotImplemented("Método não implementado")

    def sorte_de_drop(self):
        raise NotImplemented("Método não implementado")


class CaixaDraconica(Caixa):
    nome = "Caixa draconico"

    def __init__(self):
        item = choice(roupas_draconicas)
        super().__init__(item)

    def sorte_de_drop(self):
        return randint(1, 100) in range(95, 101)

    def consumir(self):
        """Método que consome a caixa e retorna um item."""
        if not self.consumida:
            self.consumida = True
            if self.sorte_de_drop():
                return self.item
            else:
                return Draconica(randint(3, 8))
        return None
