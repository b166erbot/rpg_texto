from jogo.tela.imprimir import colorir


class Npc:
    # por enquanto essa classe está sem propósito. futuramente eu irei adicionar
    # mais npcs e adicionar propósito a essa classe ou removela.
    def __init__(self, nome: str):
        self.nome = nome

# desacopla os itens para que outros módulos do código possam usá-los.
class Comerciante(Npc):
    def __init__(self, nome: str):
        super().__init__(nome)
        self.itens = {
            'poção de vida fraca': 15, 'poção de vida média': 30,
            'poção de vida grande': 45, 'poção de vida extra grande': 60,
            'elixir de vida': 100, 'elixir de vida média': 200,
            'elixir de vida grande': 300, 'elixir de vida extra grande': 400
        }

    # anotações aqui geraria bug?
    def comprar(self, item: str, quantidade: int, personagem) -> dict:
        preço = quantidade * self.itens[item]
        if personagem.inventario['pratas'] > preço:
            personagem.inventario['pratas'] -= preço
            personagem.inventario[item] = quantidade
        else:
            texto = 'compra não realizada: {}'
            print(texto.format(colorir('dinheiro insuficiente', 'vermelho')))

    def interagir(self, personagem):
        itens_dicio = dict(enumerate(tuple(self.itens), 1))  # funciona?
        itens = list(map(
            lambda x: f"{x[0]} - {colorir(x[1], 'cyan')}", itens_dicio.items()
        ))
        print('', *itens, sep='\n')
        item = int(input('O que deseja comprar?: '))
        while item:
            quantidade = int(input('Quantidade: '))
            self.comprar(itens_dicio[item], quantidade, personagem)
            print('', *itens, sep='\n')
            item = input('Deseja mais alguma coisa?: ')
