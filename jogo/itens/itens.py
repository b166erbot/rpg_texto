from itertools import groupby

from jogo.utils import Artigo, arrumar_porcentagem


class SemItemEquipado:
    def __init__(self, nome_do_equipamento, tipo, tipo_equipar):
        self.nome_do_equipamento = nome_do_equipamento
        self.tipo = tipo
        self.tipo_equipar = tipo_equipar
        self.classe = "Nenhum"
        self.bonus = []
        self.conjunto = "item comum"

    def __repr__(self):
        nome = self.nome_do_equipamento
        return f"Não há item equipado n{Artigo(nome)} {nome}"

    def __str__(self):
        nome = self.nome_do_equipamento
        return f"Não há item equipado n{Artigo(nome)} {nome}"

    def __bool__(self):
        return False


class CalcularBonus:
    def __init__(self, personagem):
        self._personagem = personagem

    def calcular(self, roupas):
        for key, equipamentos in groupby(roupas, key=lambda x: x.conjunto):
            equipamentos = list(equipamentos)
            if len(equipamentos) > 0:
                atributos = equipamentos[0].bonus
                for atributo in atributos:
                    if len(equipamentos) >= atributo.quantidade:
                        atributo.calcular(self._personagem)


class Atributo:
    def __init__(self, atributo: str, valor: int, tipo: str, quantidade: int):
        self._atributo = atributo
        self._valor = valor
        self._tipo = tipo
        # quantidade de itens equipados
        self.quantidade = quantidade

    def calcular(self, personagem):
        if self._tipo == "porcentagem":
            valor = personagem.status[self._atributo]
            adicionar_valor = (valor * self._valor) // 100
            personagem.status[self._atributo] += adicionar_valor
        elif self._tipo == "valor real":
            personagem.status[self._atributo] += self._valor

    def __repr__(self):
        if self._tipo == "porcentagem":
            return f"{self._atributo}: {self._valor}%"
        else:
            return f"{self._atributo}: {self._valor}"
