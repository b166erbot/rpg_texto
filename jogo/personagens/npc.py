from jogo.tela.imprimir import Imprimir
from jogo.itens.pocoes import curas
from time import sleep


tela = Imprimir()


class Npc:
    # por enquanto essa classe está sem propósito. futuramente eu irei adicionar
    # mais npcs e adicionar propósito a essa classe ou removela.
    def __init__(self, nome: str):
        self.nome = nome


class Comerciante(Npc):
    def __init__(self, nome: str):
        super().__init__(nome)
        self.itens = {x: y for x, y in enumerate(curas, 1)}
        self.tabela = list(map(
            lambda x: f"{x[0]} - {x[1].nome}",
            self.itens.items()
        ))

    def comprar(self, item, quantidade: int, personagem) -> dict:
        preço = quantidade * item.custo
        if int(personagem.pratas) > preço:
            personagem.pratas -= preço
            for n in range(quantidade):
                personagem.inventario.append(item())
        else:
            texto = 'compra não realizada: dinheiro insuficiente'
            tela.imprimir(texto)
            sleep(3)

    def interagir(self, personagem):
        tela.limpar_tela()
        for texto in self.tabela:
            tela.imprimir(texto + '\n')
        tela.imprimir('O que deseja comprar?: ')
        numero = tela.obter_string()
        while numero:
            tela.imprimir('Quantidade: ')
            quantidade = tela.obter_string()
            self.comprar(self.itens[int(numero)], int(quantidade), personagem)
            tela.limpar_tela()
            for texto in self.tabela:
                tela.imprimir(texto + '\n')
            tela.imprimir('Deseja mais alguma coisa?: ')
            numero = tela.obter_string()
        tela.limpar_tela()
        tela.imprimir('volte sempre!')
        sleep(1)


def funcao_quest(nome, personagem, quest):
    tela.imprimir(
        f'{nome}: Faz tempo que não vejo meu gatinho, acho que o perdi.'
    )
    tela.imprimir('Ele sempre vai brincar na floresta. Traga ele para mim')
    tela.imprimir(' que eu te dou dinheiro.\n')
    tela.imprimir('deseja aceitar a quest? s/n: ')
    resposta = tela.obter_string().lower()
    if resposta in ['s', 'sim']:
        personagem.quests.append(quest)


class Quest:
    def __init__(self, descricao, valor, item):
        self.descricao = descricao
        self.valor = valor
        self.item = item

    def pagar(self, personagem):
        personagem.pratas += self.valor


class Pessoa(Npc):
    def __init__(self, nome, quest, item, funcao_quest):
        super().__init__(nome)
        self.item = item
        self.quest = quest
        self.funcao_quest = funcao_quest
        self.missao_aceita = False
        self.missao_finalizada = False

    def missao(self, personagem):
        tela.limpar_tela()
        self.funcao_quest(self.nome, personagem, self.quest)
        self.missao_aceita = True

    def entregar_quest(self, personagem):
        if self.quest.item in personagem.inventario:
            self.quest.pagar(personagem)
            index = personagem.inventario.index(self.quest.item)
            personagem.inventario.pop(index)
            self.missao_finalizada = True
            tela.imprimir(
                f'{self.nome}: Muito obrigada. aqui está seu dinheiro'
            )

    def interagir(self, personagem):
        if not self.missao_finalizada:
            if self.missao_aceita:
                self.entregar_quest(personagem)
            else:
                self.missao(personagem)
        else:
            tela.imprimir(f"{self.nome}: não tenho mais nada a pedir.\n")
            sleep(2)
