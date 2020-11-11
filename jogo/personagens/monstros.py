from asyncio import sleep
from collections import Counter
from random import randint, choice
from jogo.tela.imprimir import Imprimir, formatar_status, colorir


class Monstro:
    # classe generica para cada monstro no jogo.
    # não importe ou use essa classe na história, só herde dela seus atributos.
    tela = Imprimir()

    def __init__(self, level = 1, status = {}):
        self.level = level
        self.experiencia = 5 * 100 // self.level
        self.status = Counter(status or
            {'vida': 100, 'dano': 3, 'resis': 5, 'velo-ataque': 1, 'critico':5,
            'armadura': 5, 'magia': 100, 'stamina': 100, 'velo-movi': 1})
        # for x in self.status:
        #     self.status[x] += self.status[x] * 100 // self.level
        self.habilidades = {}

    async def atacar(self, other):
        while all([other.status['vida'] > 0, self.status['vida'] > 0]):
            dano = self.status['dano']
            other.status['vida'] -= dano
            if other.status['vida'] < 0:
                other.status['vida'] = 0
            print() # para cada imprimir, precisa de um print. #bug#
            self.tela.imprimir(formatar_status(self))
            await sleep(0.2)
        # if self.status['vida'] > 0:
        #     # print(colorir(f"\n{self.nome} venceu!", 'verde'))
        #     self.tela.imprimir(colorir(f"- {self.nome} -  venceu!", 'verde'))
        # if self.status['vida'] > 0:
        #     self.tela.imprimir(formatar_status(self))
        print() # para cada imprimir, precisa de um print. #bug#
        self.tela.imprimir(formatar_status(self))
        await sleep(1)

    def ressucitar(self):
        self.status['vida'] = 100


class Cascudinho(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = {'investida': 4, 'garras afiadas': 6}
        self.nome = 'Cascudinho'
        self.classe = 'Monstro comum'
        self.tipo = 'Tatu bola'


# class Traquinagem(Mostro):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.habilidades = {}
#         self.nome = 'Traquinagem'
#         self.classe = 'Mostro comum'
#         self.tipo = 'trolador'
