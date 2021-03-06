from jogo.tela.imprimir import Imprimir
from jogo.itens.pocoes import curas
from time import sleep


class Npc:
    # por enquanto essa classe está sem propósito. futuramente eu irei adicionar
    # mais npcs e adicionar propósito a essa classe ou removela.
    def __init__(self, nome: str):
        self.nome = nome

# desacopla os itens para que outros módulos do código possam usá-los.
class Comerciante(Npc):
    tela = Imprimir()
    def __init__(self, nome: str):
        super().__init__(nome)
        self.itens = {x: y for x, y in enumerate(curas, 1)}
        self.tabela = list(map(
            lambda x: f"{x[0]} - {x[1].nome}",
            self.itens.items()
        ))

    # anotações aqui geraria bug? criar anotação de objeto poção?
    def comprar(self, item, quantidade: int, personagem) -> dict:
        preço = quantidade * item.custo
        if int(personagem.pratas) > preço:
            personagem.pratas.desacrescentar(preço)
            for n in range(quantidade):
                personagem.inventario.append(item())
        else:
            texto = 'compra não realizada: {}'
            print(texto.format('dinheiro insuficiente'))

    def interagir(self, personagem):
        self.tela.limpar_tela()
        for texto in self.tabela:
            self.tela.imprimir(texto + '\n')
        self.tela.imprimir('O que deseja comprar?: ')
        numero = self.tela.obter_string()
        while numero:
            self.tela.imprimir('Quantidade: ')
            quantidade = self.tela.obter_string()
            self.comprar(self.itens[int(numero)], int(quantidade), personagem)
            self.tela.limpar_tela()
            for texto in self.tabela:
                self.tela.imprimir(texto + '\n')
            self.tela.imprimir('Deseja mais alguma coisa?: ')
            numero = self.tela.obter_string()
        self.tela.limpar_tela()
        self.tela.imprimir('volte sempre!')
        sleep(1)
