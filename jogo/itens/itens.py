from jogo.utils import Substantivo


class SemItemEquipado:
    def __init__(self, nome_do_equipamento):
        self.nome_do_equipamento = nome_do_equipamento

    def __repr__(self):
        nome = self.nome_do_equipamento
        return f"Não há item equipado n{Substantivo(nome)} {nome}"

    def __str__(self):
        nome = self.nome_do_equipamento
        return f"Não há item equipado n{Substantivo(nome)} {nome}"

    def __bool__(self):
        return False
