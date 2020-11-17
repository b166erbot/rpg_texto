from asyncio import sleep
from collections import Counter
from random import randint, choice
from jogo.tela.imprimir import Imprimir, formatar_status


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
        self.habilidades = {}
        self.local_imprimir = 1

    async def atacar(self, other):
        while all([other.status['vida'] > 0, self.status['vida'] > 0]):
            dano = self.status['dano']
            other.status['vida'] -= dano
            if randint(0, 2) == 2:
                habilidade = choice(self.habilidades)
                habilidade(other)
            if other.status['vida'] < 0:
                other.status['vida'] = 0
            self.tela.imprimir_combate(formatar_status(self), self)
            await sleep(0.2)
        self.tela.imprimir_combate(formatar_status(self), self)
        await sleep(1)

    def ressucitar(self):
        self.status['vida'] = 100


class Cascudinho(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.investida, self.garras_afiadas]
        self.nome = 'Cascudinho'
        self.classe = 'Monstro comum'
        self.tipo = 'Tatu bola'

    def investida(self, other):
        other.status['vida'] -= 4

    def garras_afiadas(self, other):
        other.status['vida'] -= 6


class Traquinagem(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.trapasseiro, self.roubo]
        self.nome = 'Traquinagem'
        self.classe = 'Mostro comum'
        self.tipo = 'trolador'

    def trapasseiro(self, other):
        other.status['vida'] -= 4

    def roubo(self, other):
        other.status['vida'] -= 5
