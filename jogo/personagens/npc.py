from time import sleep

from jogo.tela.imprimir import Imprimir
from jogo.utils import Artigo, chunk

tela = Imprimir()


class Npc:
    def __init__(self, nome: str, tipo: str):
        self.nome = nome
        self.tipo = tipo

    def __str__(self):
        return f"{self.nome}[{self.tipo}]"

    def __repr__(self):
        return f"{self.nome}[{self.tipo}]"


class Comerciante(Npc):
    def __init__(self, nome: str, itens: list):
        super().__init__(nome, "Comerciante")
        self.itens = {numero: item for numero, item in enumerate(itens, 1)}
        self.tabela = [
            f"{numero} - {item.nome} ${item.preco}"
            for numero, item in self.itens.items()
        ]
        self.tabela_cortada = chunk(self.tabela, 16)
        self.salvar = False

    def comprar(self, item, quantidade: int, personagem):
        """Método que faz as compras pelo personagem."""
        preço = quantidade * item.preco
        if int(personagem.pratas) >= preço:
            personagem.pratas -= preço
            for n in range(quantidade):
                personagem.inventario.append(item())
        else:
            texto = "compra não realizada: dinheiro insuficiente"
            tela.imprimir(texto, "cyan")
            sleep(3)

    def interagir(self, personagem):
        """Método que mostra os itens e obtem o número da compra."""
        tela.limpar_tela()
        numero = self._obter_numero("O que deseja comprar?: ", personagem)
        while numero.isnumeric() and bool(numero) and int(numero) in self.itens:
            tela.imprimir("Quantidade: ", "cyan")
            quantidade = tela.obter_string()
            if not bool(quantidade):
                break
            self.comprar(self.itens[int(numero)], int(quantidade), personagem)
            tela.limpar_tela()
            numero = self._obter_numero(
                "Deseja mais alguma coisa?: ", personagem
            )
        tela.limpar_tela()
        tela.imprimir("volte sempre!", "cyan")
        sleep(1)

    def _obter_numero(self, mensagem: str, personagem):
        """Método que organiza as páginas para o usuário e retorna um numero."""
        numeros_paginas = {
            f":{n}": n for n in range(1, len(self.tabela_cortada) + 1)
        }
        numero = ":1"
        while numero in numeros_paginas:
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(self.tabela_cortada)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            tela.imprimir(f"seu dinheiro: {personagem.pratas}\n", "cyan")
            n = numeros_paginas.get(numero, 1)
            for texto in self.tabela_cortada[n - 1]:
                tela.imprimir(texto + "\n", "cyan")
            tela.imprimir(mensagem, "cyan")
            numero = tela.obter_string()
        return numero


class Pessoa(Npc):
    def __init__(self, nome: str):
        super().__init__(nome, "Pessoa do vilarejo")
        self.quest_atual = False
        self.salvar = True

    def missao(self, personagem):
        """Método que coloca a missão na tela para o personagem."""
        quests = [
            quest
            for quest in self.quests
            if all(
                [
                    not quest.finalizada,
                    not quest.iniciada,
                    quest.level <= personagem.level,
                ]
            )
        ]
        if len(quests) > 0:
            quest = quests[0]
            quest.historia()
            aceito = quest.aceitar()
            if aceito:
                personagem.quests.append(quest)
                quest.iniciada = True

    def entregar_quest(self, personagem):
        """
        Método que recebe a quest devolta, paga e da o xp para o personagem.
        """
        itens = list(
            filter(
                lambda x: self.quest_atual.item.nome == x.nome,
                personagem.inventario,
            )
        )
        quest = self.quest_atual
        if len(itens) == quest.numero_de_itens_requeridos:
            quest.pagar(personagem)
            quest.depositar_xp(personagem)
            personagem.atualizar_status()
            quests = filter(lambda q: q == quest, personagem.quests)
            for q in quests:
                index = personagem.quests.index(q)
                personagem.quests.pop(index)
            for item in itens:
                index = personagem.inventario.index(item)
                personagem.inventario.pop(index)
            self.quest_atual.finalizada = True
            tela.imprimir(
                f"{self.nome}: Muito obrigad{Artigo(self.nome)}."
                f" aqui está seu dinheiro ${self.quest_atual.valor} "
                f"xp={self.quest_atual.xp}",
                "cyan",
            )
            sleep(3)
        else:
            tela.imprimir("complete a missão e depois volte aqui", "cyan")
            sleep(2)

    def interagir(self, personagem):
        """Método que dá a quest para o personagem."""
        tela.limpar_tela()
        if not self.quest_atual or self.quest_atual.finalizada:
            self.proxima_quest(personagem.level)
        if not self.quest_atual:
            tela.imprimir(f"{self.nome}: não tenho mais nada a pedir.", "cyan")
            if len(self._obter_quests_nao_iniciadas2(personagem.level)):
                tela.imprimir(" volte quando tiver mais level\n", "cyan")
            sleep(2)
            return
        if self.quest_atual.iniciada and not self.quest_atual.finalizada:
            self.entregar_quest(personagem)
        else:
            self.missao(personagem)

    def receber_quest(self, quests: list):
        """Método que recebe as quests."""
        quests = sorted(quests, key=lambda quest: quest.level)
        self.quests = quests
        self.proxima_quest(1)

    def proxima_quest(self, level):
        """Método que define a próxima quest."""
        if not self.quest_atual:
            self._definir_proxima_quest(level)
        else:
            if self.quest_atual.finalizada:
                self._definir_proxima_quest(level)

    def _definir_proxima_quest(self, level):
        """Método auxiliar que define a proxima quest."""
        quests = self._obter_quests_nao_iniciadas(level)
        if len(quests):
            self.quest_atual = quests[0]
        else:
            self.quest_atual = False

    def _obter_quests_nao_iniciadas(self, level):
        """Método que retorna as quests não iniciadas do level pra baixo."""
        return [
            quest
            for quest in self.quests
            if not quest.iniciada and quest.level <= level
        ]

    def _obter_quests_nao_iniciadas2(self, level):
        """Método que retorna as quests não iniciadas do level pra cima"""
        return [
            quest
            for quest in self.quests
            if not quest.iniciada and quest.level > level
        ]


class Banqueiro(Npc):
    def __init__(self, nome: str):
        super().__init__(nome, "Banqueiro")
        self.nome = nome
        self.salvar = True
        self.tamanho_do_inventario = 30
        self.inventario = []

    def guardar_item(self, item, personagem):
        """Método que guarda um item no inventario do banqueiro."""
        if len(self.inventario) < self.tamanho_do_inventario:
            self.inventario.append(item)
            index = personagem.inventario.index(item)
            personagem.inventario.pop(index)
        else:
            tela.imprimir("inventario do banqueiro cheio.")
            sleep(2)

    def retirar(self, item, personagem):
        """Método que retira um item do inventario do banqueiro."""
        index = self.inventario.index(item)
        self.inventario.pop(index)
        personagem.inventario.append(item)

    def interagir(self, personagem):
        """Método que interage com o personagem."""
        tela.limpar_tela()
        tela.imprimir("1 -> guardar, 2 -> adquirir\n")
        tela.imprimir("deseja guardar ou adquirir um item?: ")
        numero = tela.obter_string()
        while numero.isnumeric():
            if numero == "1":
                item = self._obter_equipamentos_personagem(
                    "deseja guardar qual item?: ", personagem
                )
                if bool(item):
                    self.guardar_item(item, personagem)
            elif numero == "2":
                item = self._obter_equipamentos_banqueiro(
                    "deseja obter qual item?: ", personagem
                )
                if bool(item):
                    self.retirar(item, personagem)
            tela.limpar_tela()
            tela.imprimir("1 -> guardar, 2 -> adquirir\n")
            tela.imprimir("deseja guardar ou adquirir um item?: ")
            numero = tela.obter_string()

    def _obter_equipamentos_personagem(self, mensagem: str, personagem):
        """Método que organiza as páginas para o usuário e retorna um item."""
        itens = list(enumerate(personagem.inventario))
        itens_dict = {str(numero): item for numero, item in itens}
        if len(itens) == 0:
            tela.imprimir("você não tem itens no inventario.", "cyan")
            sleep(2)
            return ""
        itens = chunk(itens, 18)
        numeros_paginas = {f":{n}": n for n in range(1, len(itens) + 1)}
        numero = ":1"
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(itens)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in itens[n - 1]:
                mensagem2 = f"{numero} - {item}"
                tela.imprimir(mensagem2 + "\n")
            tela.imprimir(mensagem, "cyan")
            numero = tela.obter_string()
        item = itens_dict.get(numero)
        return item

    def _obter_equipamentos_banqueiro(self, mensagem: str, personagem):
        """Método que organiza as páginas para o usuário e retorna um item."""
        itens = list(enumerate(self.inventario))
        itens_dict = {str(numero): item for numero, item in itens}
        if len(itens) == 0:
            tela.imprimir(
                "você não tem itens no inventario do banqueiro.", "cyan"
            )
            sleep(2)
            return ""
        itens = chunk(itens, 18)
        numeros_paginas = {f":{n}": n for n in range(1, len(itens) + 1)}
        numero = ":1"
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(itens)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in itens[n - 1]:
                mensagem2 = f"{numero} - {item}"
                tela.imprimir(mensagem2 + "\n")
            tela.imprimir(mensagem, "cyan")
            numero = tela.obter_string()
        item = itens_dict.get(numero)
        return item
