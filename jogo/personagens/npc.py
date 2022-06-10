from time import sleep

from jogo.itens.pocoes import curas
from jogo.tela.imprimir import Imprimir
from jogo.utils import Substantivo, chunk

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
    def __init__(self, nome: str):
        super().__init__(nome, 'Comerciante')
        self.itens = {x: y for x, y in enumerate(curas, 1)}
        self.tabela = [
            f"{numero} - {item.nome} ${item.custo}"
            for numero, item in self.itens.items()
        ]
        self.tabela_cortada = chunk(self.tabela, 16)

    def comprar(self, item, quantidade: int, personagem):
        """Método que faz as compras pelo personagem."""
        preço = quantidade * item.custo
        if int(personagem.pratas) > preço:
            personagem.pratas -= preço
            for n in range(quantidade):
                personagem.inventario.append(item())
        else:
            texto = 'compra não realizada: dinheiro insuficiente'
            tela.imprimir(texto, 'cyan')
            sleep(3)

    def interagir(self, personagem):
        """Método que mostra os itens e obtem o número da compra."""
        tela.limpar_tela()
        numero = self._obter_numero('O que deseja comprar?: ', personagem)
        while numero.isnumeric() and bool(numero) and int(numero) in self.itens:
            tela.imprimir('Quantidade: ', 'cyan')
            quantidade = tela.obter_string()
            if not bool(quantidade):
                break
            self.comprar(self.itens[int(numero)], int(quantidade), personagem)
            tela.limpar_tela()
            numero = self._obter_numero(
                'Deseja mais alguma coisa?: ', personagem
            )
        tela.limpar_tela()
        tela.imprimir('volte sempre!', 'cyan')
        sleep(1)

    def _obter_numero(self, mensagem: str, personagem):
        """Método que organiza as páginas para o usuário e retorna um numero."""
        numeros_paginas = {
            f":{n}": n for n in range(1, len(self.tabela_cortada) + 1)
        }
        numero = ':1'
        while numero in numeros_paginas:
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(self.tabela_cortada)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                'cyan'
            )
            tela.imprimir(f"seu dinheiro: {personagem.pratas}\n", 'cyan')
            n = numeros_paginas.get(numero, 1)
            for texto in self.tabela_cortada[n -1]:
                tela.imprimir(texto + '\n', 'cyan')
            tela.imprimir(mensagem, 'cyan')
            numero = tela.obter_string()
        return numero


class Pessoa(Npc):
    def __init__(self, nome):
        super().__init__(nome, 'Pessoa do vilarejo')
        self.quest_atual = False

    def missao(self, personagem):
        """Método que coloca a missão na tela para o personagem."""
        quests = [
            quest_status for quest_status
            in self.quests
            if all([
                not quest_status.finalizada, not quest_status.iniciada,
                quest_status.quest.level <= personagem.level
            ])
        ]
        if len(quests) > 0:
            quest_status = quests[0]
            quest_status.quest.historia()
            aceito = quest_status.quest.aceitar()
            if aceito:
                personagem.quests.append(quest_status.quest)
                quest_status.iniciada = True

    def entregar_quest(self, personagem):
        """
            Método que recebe a quest devolta, paga e da o xp para o personagem.
        """
        if not self.quest_atual:
            self.proxima_quest(personagem.level)
        itens = [
            x for x in
            personagem.inventario
            if self.quest_atual.quest.item.nome == x.nome
        ]
        quest = self.quest_atual.quest
        if len(itens) == quest.numero_de_itens_requeridos:
            quest.pagar(personagem)
            quest.depositar_xp(personagem)
            index = personagem.quests.index(quest)
            personagem.quests.pop(index)
            for item in itens:
                index = personagem.inventario.index(item)
                personagem.inventario.pop(index)
            self.quest_atual.finalizada = True
            tela.imprimir(
                f'{self.nome}: Muito obrigad{Substantivo(self.nome)}.'
                ' aqui está seu dinheiro', 'cyan'
            )
            sleep(3)
        else:
            tela.imprimir('finalize a missão e depois volte aqui', 'cyan')
            sleep(2)

    def interagir(self, personagem):
        """Método que dá a quest para o personagem."""
        if not self.quest_atual or self.quest_atual.finalizada:
            self.proxima_quest(personagem.level)
        if not self.quest_atual:
            tela.imprimir(
                f"{self.nome}: não tenho mais nada a pedir.\n", 'cyan'
            )
            sleep(2)
            return
        if self.quest_atual.iniciada and not self.quest_atual.finalizada:
            self.entregar_quest(personagem)
        else:
            self.missao(personagem)

    def receber_quest_status(self, quests: list):
        quests = sorted(quests, key=lambda x: x.quest.level)
        self.quests = quests
        self.proxima_quest(1)

    def proxima_quest(self, level):
        if not self.quest_atual:
            self._definir_proxima_quest(level)
        else:
            if self.quest_atual.finalizada:
                self._definir_proxima_quest(level)

    def _definir_proxima_quest(self, level):
        quests = self._obter_quests_nao_iniciadas(level)
        if len(quests):
            self.quest_atual = quests[0]
        else:
            self.quest_atual = False

    def _obter_quests_nao_iniciadas(self, level):
        return [
            quest_status
            for quest_status
            in self.quests
            if not quest_status.iniciada
            and quest_status.quest.level <= level
        ]
