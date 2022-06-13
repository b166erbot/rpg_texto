from jogo.utils import Artigo


class SemItemEquipado:
    def __init__(self, nome_do_equipamento):
        # nome_do_equipamento precisa ser obrigatoriamente o tipo do item
        self.nome_do_equipamento = nome_do_equipamento
        self.tipo = nome_do_equipamento
        self.classe = "Nenhum"

    def __repr__(self):
        nome = self.nome_do_equipamento
        return f"Não há item equipado n{Artigo(nome)} {nome}"

    def __str__(self):
        nome = self.nome_do_equipamento
        return f"Não há item equipado n{Artigo(nome)} {nome}"

    def __bool__(self):
        return False
