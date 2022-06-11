from random import randint

from jogo.itens.quest import ItemQuest
from jogo.tela.imprimir import Imprimir

tela = Imprimir()


class Quest:
    def __init__(self, descricao, valor, xp, item, level):
        # coloque uma descrição pequena
        self.descricao = descricao
        self.valor = valor
        self.item = item
        self.xp = xp
        self.level = level
        self.numero_de_itens_requeridos = 1

    def pagar(self, personagem):
        """Método que paga o personagem."""
        personagem.pratas += self.valor

    def depositar_xp(self, personagem):
        """Método que dá o xp para o personagem."""
        personagem.experiencia += self.xp

    def historia(self):
        raise NotImplementedError("Método não implementado.")

    def aceitar(self) -> bool:
        tela.imprimir("deseja aceitar a quest? s/n: ", "cyan")
        resposta = tela.obter_string().lower()
        if resposta in ["s", "sim"]:
            return True
        return False

    def __repr__(self):
        return f"Quest({self.descricao}, valor={self.valor}, xp={self.xp})"

    def sorte_de_drop(self):
        raise NotImplementedError("Método não implementado")


class QuestGato(Quest):
    def __init__(self, nome_do_npc: str):
        self.nome_do_npc = nome_do_npc
        item = ItemQuest("gatinho")
        super().__init__("pegar o gatinho", 150, 1000, item, 1)

    def historia(self):
        tela.limpar_tela()
        tela.imprimir(
            f"{self.nome_do_npc}: Faz tempo que não vejo meu gatinho, "
            "acho que o perdi. "
            "Ele sempre vai brincar na floresta. Traga ele para mim "
            f"que eu te dou dinheiro. ${self.valor}\n",
            "cyan",
        )

    def sorte_de_drop(self):
        return randint(1, 7) == 1


class QuestLenha(Quest):
    def __init__(self, nome_do_npc: str):
        self.nome_do_npc = nome_do_npc
        item = ItemQuest("galho")
        super().__init__("pegar lenha", 150, 1000, item, 1)
        self.numero_de_itens_requeridos = 5

    def historia(self):
        tela.limpar_tela()
        tela.imprimir(
            f"{self.nome_do_npc}: Eu estou precisando de um pouco de lenha"
            f". Tem como você pegar um pouco para mim? ${self.valor}\n",
            "cyan",
        )

    def sorte_de_drop(self):
        return randint(1, 5) == 1


class QuestStatus:
    """classe que salva o status de uma quest no personagem."""

    def __init__(self, quest):
        # self.nome = nome
        self.quest = quest
        self.iniciada = False
        self.finalizada = False


quests_da_lorena = [QuestGato, QuestLenha]
