from collections import Counter
from asyncio import sleep
from jogo.tela.imprimir import formatar_status, colorir, imprimir
from screen import Screen


tela = Screen()


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

    def __init__(
        self, nome, jogador = 'bot', level = 1, status = {}, atributos = {}
    ):
        self.nome = nome
        self.status = Counter(status or
            {'vida': 100, 'dano': 5, 'resis': 5, 'velo-ataque': 1, 'criti': 5,
             'armadura': 5, 'magia': 100, 'stamina': 100, 'velo-movi': 1})
        self.atributos = Counter(status or
            {'vitalidade': 0, 'fortividade': 0, 'inteligência': 0,
             'crítico': 0, 'destreza': 0, 'resistência': 0, 'movimentação': 0}
        )
        self.level = level
        self.habilidades = {}
        self.habi = 'dano'
        self.jogador = jogador
        # self.quantidade_habilidades = ''

    def atacar(self, other, ciclo):
        if self.jogador != 'humano':
            return self._atacar_como_bot(other, ciclo)
        return self._atacar_como_jogador(other, ciclo)

    async def _atacar_como_bot(self, other, ciclo):
        while all([other.status['vida'] > 0, self.status['vida'] > 0]):
            dano = self.status[self.habi] * 100
            other.status['vida'] -= dano // self.habilidades.get(self.habi, 100)
            self.habi = 'dano'
            imprimir(formatar_status(self), ciclo, tela)
            await sleep(0.1)
        if self.status['vida'] > 0:
            print(colorir(f"\n{self.nome} venceu!", 'verde'))
        else:
            imprimir(formatar_status(self), ciclo, tela)
        await sleep(0.1)

    async def _atacar_como_jogador(self, other, ciclo):
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
