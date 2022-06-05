from jogo.tela.imprimir import Imprimir
from jogo.itens.pocoes import curas
from jogo.utils import Substantivo
from time import sleep


tela = Imprimir()


class Npc:
    def __init__(self, nome: str):
        self.nome = nome


class Comerciante(Npc):
    def __init__(self, nome: str):
        super().__init__(nome)
        self.itens = {x: y for x, y in enumerate(curas, 1)}
        self.tabela = [
            f"{numero} - {item.nome}" for numero, item in self.itens.items()
        ]

    def comprar(self, item, quantidade: int, personagem):
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
        while all([bool(numero), numero.isnumeric()]):
            tela.imprimir('Quantidade: ')
            quantidade = tela.obter_string()
            if not bool(quantidade):
                break
            self.comprar(self.itens[int(numero)], int(quantidade), personagem)
            tela.limpar_tela()
            for texto in self.tabela:
                tela.imprimir(texto + '\n')
            tela.imprimir('Deseja mais alguma coisa?: ')
            numero = tela.obter_string()
        tela.limpar_tela()
        tela.imprimir('volte sempre!')
        sleep(1)


class Quest:
    def __init__(self, descricao, valor, xp, item):
        self.descricao = descricao
        self.valor = valor
        self.item = item
        self.xp = xp

    def pagar(self, personagem):
        personagem.pratas += self.valor

    def depositar_xp(self, personagem):
        personagem.experiencia += self.xp


class Pessoa(Npc):
    def __init__(self, nome, quest, funcao_quest, mensagem):
        super().__init__(nome)
        self.quest = quest
        self.funcao_quest = funcao_quest
        self.missao_aceita = False
        self.missao_finalizada = False
        self.mensagem = mensagem
        self.volta = False

    def missao(self, personagem):
        tela.limpar_tela()
        missao = self.funcao_quest(self.nome, personagem, self.quest)
        self.missao_aceita = missao

    def entregar_quest(self, personagem):
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
                ' aqui está seu dinheiro'
            )
            sleep(3)
        else:
            tela.imprimir(self.mensagem)
            sleep(3)

    def interagir(self, personagem):
        if not self.missao_finalizada:
            if self.missao_aceita:
                self.entregar_quest(personagem)
            elif not self.volta:
                self.missao(personagem)
            else:
                tela.imprimir(f"{self.nome}: não tenho mais nada a pedir.\n")
                sleep(2)
        else:
            tela.imprimir(f"{self.nome}: não tenho mais nada a pedir.\n")
            sleep(2)
