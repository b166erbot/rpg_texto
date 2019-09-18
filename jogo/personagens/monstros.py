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
            if randint(0, 1):
                keys = tuple(self.habilidades)
                # dano = dano * 100 // self.habilidades[choice(keys)]  # dano errado
                dano = self.habilidades[choice(keys)]
            other.status['vida'] -= dano
            if other.status['vida'] < 0:
                other.status['vida'] = 0
            self.tela.imprimir(formatar_status(self))
            await sleep(0.1)
        if self.status['vida'] > 0:
            print(colorir(f"\n{self.nome} venceu!", 'verde'))
        else:
            self.tela.imprimir(formatar_status(self))
        self.tela.reiniciar_ciclo_menos_1()
        await sleep(1)
        self.tela.limpar_tela()

    def ressucitar(self):
        self.status['vida'] = 100


class Cascudinho(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = {'investida': 4, 'garras afiadas': 6}
        self.nome = 'Cascudinho'
        self.classe = 'Monstro comum'
        self.tipo = 'Tatu bola'
