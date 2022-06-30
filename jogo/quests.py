from random import randint

from jogo.itens.quest import ItemQuest
from jogo.tela.imprimir import Imprimir

tela = Imprimir()


class Quest:
    def __init__(
        self,
        descricao,
        valor,
        xp,
        item,
        numero_de_itens_requeridos,
        level,
        tipo,
        monstro_drop=False,
    ):
        # coloque uma descrição pequena
        self.descricao = descricao
        self.valor = valor
        self.xp = xp
        self.item = item
        self.numero_de_itens_requeridos = numero_de_itens_requeridos
        self.level = level
        self.tipo = tipo
        self.monstro = monstro_drop
        self.iniciada = False
        self.finalizada = False

    def pagar(self, personagem):
        """Método que paga o personagem."""
        personagem.moedas["Pratas"] += self.valor

    def depositar_xp(self, personagem):
        """Método que dá o xp para o personagem."""
        personagem.experiencia.depositar_valor(self.xp)

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

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                f"não consigo igualar quest com um tipo: {other.__class__}"
            )
        condicoes = [
            self.descricao == other.descricao,
            self.valor == other.valor,
            self.item == other.item,
            self.xp == other.xp,
            self.level == other.level,
            (
                self.numero_de_itens_requeridos
                == other.numero_de_itens_requeridos
            ),
            self.tipo == other.tipo,
            self.monstro == other.monstro,
            self.iniciada == other.iniciada,
            self.finalizada == other.finalizada,
        ]
        if all(condicoes):
            return True
        else:
            return False


class QuestGato(Quest):
    def __init__(self, nome_do_npc: str):
        self.nome_do_npc = nome_do_npc
        item = ItemQuest("gatinho")
        super().__init__("pegar o gatinho", 150, 250, item, 1, 1, "mapa")

    def historia(self):
        tela.limpar_tela()
        tela.imprimir(
            f"{self.nome_do_npc}: Faz tempo que não vejo meu gatinho, "
            "acho que o perdi. "
            "Ele sempre vai brincar na floresta. Traga ele para mim "
            f"que eu te dou dinheiro. ${self.valor} xp={self.xp}\n",
            "cyan",
        )

    def sorte_de_drop(self):
        return randint(1, 7) == 1


class QuestLenha(Quest):
    def __init__(self, nome_do_npc: str):
        self.nome_do_npc = nome_do_npc
        item = ItemQuest("galho")
        super().__init__("pegar lenha", 150, 250, item, 5, 1, "mapa")

    def historia(self):
        tela.limpar_tela()
        tela.imprimir(
            f"{self.nome_do_npc}: Eu estou precisando de um pouco de lenha"
            f". Tem como você pegar um pouco para mim? ${self.valor} "
            f"xp={self.xp}\n",
            "cyan",
        )

    def sorte_de_drop(self):
        return randint(1, 5) == 1


class QuestUnhas(Quest):
    def __init__(self, nome_do_npc: str):
        self.nome_do_npc = nome_do_npc
        item = ItemQuest("Unha de Tamandua")
        super().__init__(
            "unha de tamandua", 150, 500, item, 3, 2, "monstro", "Tamandua"
        )

    def historia(self):
        tela.limpar_tela()
        tela.imprimir(
            f"{self.nome_do_npc}: Você tem unhas de tamanduá? Eu "
            "estou precisando para fazer uma poção. Traga 3 pra "
            f"mim. ${self.valor} xp={self.xp}\n",
            "cyan",
        )

    def sorte_de_drop(self):
        return randint(1, 3) == 1


quests_da_lorena = [QuestGato, QuestLenha]

quests_do_eivor = [QuestUnhas]
