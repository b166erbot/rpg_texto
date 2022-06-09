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
    def __init__(self, nome, quest, funcao_quest, mensagem):
        super().__init__(nome, 'Pessoa do vilarejo')
        self.quest = quest
        self.funcao_quest = funcao_quest
        self.missao_aceita = False
        self.missao_finalizada = False
        self.mensagem = mensagem

    def missao(self, personagem):
        """Método que coloca a missão na tela para o personagem."""
        tela.limpar_tela()
        missao = self.funcao_quest(self.nome, personagem, self.quest)
        self.missao_aceita = missao

    def entregar_quest(self, personagem):
        """
            Método que recebe a quest devolta, paga e da o xp para o personagem.
        """
        if self.quest.item in personagem.inventario:
            self.quest.pagar(personagem)
            self.quest.depositar_xp(personagem)
            index = personagem.quests.index(self.quest)
            personagem.quests.pop(index)
            index = personagem.inventario.index(self.quest.item)
            personagem.inventario.pop(index)
            self.missao_finalizada = True
            tela.imprimir(
                f'{self.nome}: Muito obrigad{Substantivo(self.nome)}.'
                ' aqui está seu dinheiro', 'cyan'
            )
            sleep(3)
        else:
            tela.imprimir(self.mensagem, 'cyan')
            sleep(3)

    def interagir(self, personagem):
        """Método que dá a quest para o personagem."""
        if not self.missao_finalizada:
            if self.missao_aceita:
                self.entregar_quest(personagem)
            elif not self.missao_aceita:
                self.missao(personagem)
            else:
                tela.imprimir(
                    f"{self.nome}: não tenho mais nada a pedir.\n", 'cyan'
                )
                sleep(2)
        else:
            tela.imprimir(
                f"{self.nome}: não tenho mais nada a pedir.\n", 'cyan'
            )
            sleep(2)
