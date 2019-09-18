from collections import Counter
from asyncio import sleep
from jogo.tela.imprimir import formatar_status, colorir, Imprimir
from screen import Screen


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
        self, nome, jogador = 'bot', level = 1, status = {}, atributos = {},
        experiencia = 0
    ):
        self.nome = nome
        self.level = level
        self.experiencia = experiencia
        self.status = Counter(status or
            {'vida': 100, 'dano': 5, 'resis': 5, 'velo-ataque': 1, 'criti': 5,
             'armadura': 5, 'magia': 100, 'stamina': 100, 'velo-movi': 1})
        self.atributos = Counter(status or
            {'vitalidade': 0, 'fortividade': 0, 'inteligência': 0,
             'crítico': 0, 'destreza': 0, 'resistência': 0, 'movimentação': 0}
        )
        # for x in self.status:
        #     self.status[x] += self.status[x] * 100 // self.level  # teste
        self.habilidades = {}
        self.inventario = {'pratas': 1500}
        self.habi = 'dano'
        self.jogador = jogador
        # self.quantidade_habilidades = ''

    def atacar(self, other):
        if self.jogador != 'humano':
            return self._atacar_como_bot(other)
        return self._atacar_como_jogador(other)

    async def _atacar_como_bot(self, other):
        while all([other.status['vida'] > 0, self.status['vida'] > 0]):
            dano = self.status[self.habi] * 100
            other.status['vida'] -= dano // self.habilidades.get(self.habi, 100)
            if other.status['vida'] < 0:
                other.status['vida'] = 0
            self.habi = 'dano'
            self.tela.imprimir(formatar_status(self))
            await sleep(0.1)
        if self.status['vida'] > 0:
            print(colorir(f"\n{self.nome} venceu!", 'verde'))
        else:
            self.tela.imprimir(formatar_status(self))
        self.tela.reiniciar_ciclo_menos_1()
        await sleep(1)
        self.tela.limpar_tela()

    async def _atacar_como_jogador(self, other):
        raise NotImplementedError()

    def ressucitar(self):
        self.status['vida'] = 100

    # async def escolher_habilidade(self, habilidade=1):
    #     if habilidade in self.quantidade_habilidades:
    #         self.habilidade_ = list(self.habilidades)[habilidade - 1]
    #     await sleep(0.01)


class Arqueiro(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self.habilidades = {'flecha de fogo': 10, 'tres flechas': 15}
        self.classe = 'Arqueiro'
        self.quantidade_habilidades = range(1, 3)


class Guerreiro(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self.habilidades = {'investida': 10, 'esmagar': 15}
        self.classe = 'Guerreiro'
        self.quantidade_habilidades = range(1, 3)


class Mago(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self.habilidades = {'bola de fogo': 10, 'bola de gelo': 10}
        self.classe = 'Mago'
        self.quantidade_habilidades = range(1, 3)


class Assassino(Humano):
    def __init__(self, nome):
        super().__init__(nome)
        self.habilidades = {}
        self.classe = 'Assassino'
        self.quantidade_habilidades = range(1, 3)


class Clerigo(Humano):  # curandeiro?
    def __init__(self, nome):
        super().__init__(nome)
        self.habilidades = {}
        self.classe = 'Clerigo'
        self.quantidade_habilidades = range(1, 3)


# druida?
# dual blade?
# lutador?  não me parece uma boa