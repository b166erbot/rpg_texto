from asyncio import sleep
from collections import Counter
from random import randint, choice
from jogo.tela.imprimir import Imprimir, formatar_status


tela = Imprimir()


class Monstro:
    def __init__(self, level = 1, status = {}):
        self.level = level
        self.experiencia = 5 * 100 // self.level
        self.status = Counter(status or
            {'vida': 100, 'dano': 3, 'resis': 5, 'velo-ataque': 1, 'critico':5,
            'armadura': 5, 'magia': 100, 'stamina': 100, 'velo-movi': 1})
        self.habilidades = {}
        self.vida_ = self.status['vida']

    async def atacar(self, other):
        while all([other.status['vida'] > 0, self.status['vida'] > 0]):
            dano = self.status['dano']
            other.receber_dano(dano, self.tipo_dano)
            if randint(0, 2) == 2:
                habilidade = choice(self.habilidades)
                if self.status['stamina'] >= 20:
                    self.status['stamina'] -= 20
                    habilidade(other)
            other.arrumar_vida()
            tela.imprimir_combate(formatar_status(self), 2)
            await sleep(0.5)
        tela.imprimir_combate(formatar_status(self), 2)
        await sleep(0.5)

    def ressucitar(self):
        self.status['vida'] = self.vida_

    @property
    def vida_maxima(self):
        return self.vida_

    def arrumar_vida(self):
        if self.status['vida'] < 0:
            self.status['vida'] = 0
        if self.status['vida'] > self.vida_maxima:
            self.status['vida'] = self.vida_maxima

class Cascudinho(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.investida, self.garras_afiadas]
        self.nome = 'Cascudinho'
        self.classe = 'Monstro comum'
        self.tipo = 'Tatu bola'
        self.tipo_dano = 'fisico'

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
        self.tipo_dano = 'fisico'

    def trapasseiro(self, other):
        other.status['vida'] -= 4

    def roubo(self, other):
        other.status['vida'] -= 5


class Topera_boss(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.pulo_fatal, self.terremoto]
        self.nome = 'Topera-boss'
        self.classe = 'Monstro chefe'
        self.tipo = 'boss'
        self.tipo_dano = 'fisico'

    def pulo_fatal(self, other):
        other.status['vida'] -= 7

    def terremoto(self, other):
        other.status['vida'] -= 10
