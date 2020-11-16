from collections import Counter
from asyncio import sleep
from random import randint, choice
from jogo.tela.imprimir import formatar_status, Imprimir
from jogo.itens.moedas import Pratas


class Humano:
    """
    Classe geral para cada classe no jogo.

    o que os atributos aumentão?
    vitalidade - vida
    fortividade - dano físico
    resistência - resistência a magia[fogo, raio, veneno, magia do submundo]
    inteligência - dano mágico
    crítico - dano crítico
    destreza - velocidade ataque, habilidade com armas
    movimentação - velocidade movimentação
    """
    # não importe ou use essa classe na história, só herde dela seus atributos.
    tela = Imprimir()

    def __init__(
        self, nome, jogador=False, level=1, status={}, atributos={},
        experiencia=0
    ):
        self.nome = nome
        self.level = level
        self.experiencia = experiencia
        self.status = Counter(
            status or {
                'vida': 100, 'dano': 5, 'resis': 5, 'velo-ataque': 1,
                'criti': 5, 'armadura': 5, 'magia': 100, 'stamina': 100,
                'velo-movi': 1
            }
        )
        self.atributos = Counter(
            status or {
                'vitalidade': 0, 'fortividade': 0, 'inteligência': 0,
                'crítico': 0, 'destreza': 0, 'resistência': 0, 'movimentação': 0
            }
        )
        self.habilidades = {}
        self.inventario = []
        self.pratas = Pratas(1500)
        self.habi = 'dano'
        self.jogador = jogador
        self.local_imprimir = 0

    def atacar(self, other):
        if self.jogador:
            return self._atacar_como_jogador(other)
        return self._atacar_como_bot(other)

    async def _atacar_como_bot(self, other):
        while all([other.status['vida'] > 0, self.status['vida'] > 0]):
            self._consumir_pocoes_bot()
            dano = self.status['dano']
            other.status['vida'] -= dano
            if other.status['vida'] < 0:
                other.status['vida'] = 0
            self.tela.imprimir_combate(formatar_status(self), self)
            await sleep(0.2)
        self.tela.imprimir_combate(formatar_status(self), self)
        await sleep(1)

    async def _atacar_como_jogador(self, other):
        # raise NotImplementedError()
        while all([other.status['vida'] > 0, self.status['vida'] > 0]):
            self._consumir_pocoes_bot()
            dano = self.status['dano']
            other.status['vida'] -= dano
            caracter = self.tela.obter_caracter()
            if caracter != -1:
                habilidade = self.habilidades[int(chr(caracter))]
                habilidade(other)
            if other.status['vida'] < 0:
                other.status['vida'] = 0
            self.tela.imprimir_combate(formatar_status(self), self)
            await sleep(0.2)
        self.tela.imprimir_combate(formatar_status(self), self)
        await sleep(1)

    def ressucitar(self):
        self.status['vida'] = 100

    def _consumir_pocoes_bot(self):
        pocoes = self._achar_pocoes()
        if all((self.status['vida'] <= 30, pocoes)):
            self.status['vida'] += pocoes[0].consumir()
            if self.status['vida'] > 100:
                self.status['vida'] = 100

    def _achar_pocoes(self) -> list:
        nomes = [
            'poção de vida fraca', 'poção de vida média',
            'poção de vida grande', 'poção de vida extra grande',
            'elixir de vida fraca', 'elixir de vida média',
            'elixir de vida grande', 'elixir de vida extra grande'
        ]
        poções = [x for x in self.inventario if x.nome in nomes]
        poções = sorted(poções, key=lambda x: x.pontos_cura)
        return poções


class Arqueiro(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self._habilidades = [self.flecha, self.tres_flechas]
        self.habilidades = dict(enumerate(self._habilidades, 1))
        self.classe = 'Arqueiro'
        self.quantidade_habilidades = range(1, 3)

    def flecha(self, other):
        other.status['vida'] -= 10

    def tres_flechas(self, other):
        other.status['vida'] -= 15


class Guerreiro(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._habilidades = [self.investida, self.esmagar]
        self.habilidades = dict(enumerate(self._habilidades, 1))
        self.classe = 'Guerreiro'
        self.quantidade_habilidades = range(1, 3)

    def investida(self, other):
        other.status['vida'] -= 10

    def esmagar(self, other):
        other.status['vida'] -= 15


class Mago(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._habilidades = [self.bola_de_fogo, self.lanca_de_gelo]
        self.habilidades = dict(enumerate(self._habilidades, 1))
        self.classe = 'Mago'
        self.quantidade_habilidades = range(1, 3)

    def bola_de_fogo(self, other):
        other.status['vida'] -= 10

    def lanca_de_gelo(self, other):
        other.status['vida'] -= 10


class Assassino(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._habilidades = [self.lancar_faca, self.ataque_furtivo]
        self.habilidades = dict(enumerate(self._habilidades, 1))
        self.habilidades = {}
        self.classe = 'Assassino'
        self.quantidade_habilidades = range(1, 3)

    def lancar_faca(self, other):
        other.status['vida'] -= 10

    def ataque_furtivo(self, other):
        other.status['vida'] -= 15


class Clerigo(Humano):  # curandeiro?
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._habilidades = [self.curar, self.luz]
        self.habilidades = dict(enumerate(self._habilidades, 1))
        self.classe = 'Clerigo'
        self.quantidade_habilidades = range(1, 3)

    def curar(self, other):
        self.status['vida'] += 25

    def luz(self, other):
        other.status['vida'] -= 10


# druida?
# dual blade?
# lutador?  não me parece uma boa
