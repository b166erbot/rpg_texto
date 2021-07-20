from random import randint, choice
from time import sleep
from re import compile
from jogo.personagens.monstros import Cascudinho, Traquinagem, Topera_boss
from jogo.assincrono.combate import combate
from jogo.tela.imprimir import efeito_digitando, Imprimir
from jogo.itens.pocoes import curas
from jogo.itens.vestes import tudo as vestes, Roupa, Anel
from jogo.itens.armas import tudo as armas, Arma


def local_linear(passagens, locais):
    fluxo = []
    for n in range(randint(2, 5)):
        passagem = choice(passagens)
        fluxo.append(f"entrando em {passagem}")
    passagem = choice(locais)
    fluxo.append(f"entrando em {passagem}")
    return fluxo


def gerar_fluxo():
    passagens = [
        'bifurcação', 'área aberta', 'passagem estreita',
        'área com pedregulhos', 'lago subterraneo'
    ]
    locais = [
        'local estreito e sem saída', 'mineiração', 'local sem saída',
        'cachoeira interna'
    ]
    fluxo = (
        local_linear(passagens, locais) + local_linear(passagens, locais)
        + local_linear(passagens, locais)
    )
    return fluxo


tela = Imprimir()


class Caverna:
    """ Classe que constroi uma caverna com caminhos aleatórios. """
    def __init__(self, nome_caverna: str, personagem):
        self.nome = nome_caverna
        self.personagem = personagem
        self._caminho = gerar_fluxo()
        self._mostros = [Cascudinho, Traquinagem]
        self._locais = [
            'local estreito e sem saída', 'mineiração', 'local sem saída',
            'cachoeira interna'
        ]
        self._substituir = compile('entrando em ').sub  # noqa

    def explorar(self):
        tela.limpar_tela()
        tela.imprimir(
            'Esta caverna é difícil, necessita de algumas poções de vida'
            '. Recomendo comprar 10 poções de vida média.'
        )
        tela.imprimir(
            f'deseja explorar a caverna: {self.nome} s/n?\n'
        )
        if tela.obter_string().lower() == 's':
            for x in self._caminho:
                efeito_digitando(x)
                if self._substituir('', x) in self._locais:
                    morto = self.sortear_inimigos()
                    if morto:
                        self.morto()
                        return
                    self.sortear_loot()
                    tela.limpar_tela()
            boss = Topera_boss(status = {
                'vida': 300, 'dano': 5, 'resis': 15, 'velo-ataque': 1,
                'critico':15, 'armadura': 15, 'magia': 100, 'stamina': 100,
                'velo-movi': 1}
            )
            combate(self.personagem, boss)
            if self.personagem.status['vida'] == 0:
                self.morto()
                return
            elif self.personagem.status['vida'] > 0:
                self.personagem.experiencia += boss.experiencia
            self.sortear_loot()
            tela.limpar_tela()
            tela.limpar_tela2()
        self.personagem.recuperar_magia_stamina()
        self.personagem.status['vida'] = 100


    def sortear_inimigos(self):
        if randint(0, 1):
            efeito_digitando('Monstros encontrados.')
            sleep(1)
            tela.limpar_tela()
            for y in range(randint(1, 3)):
                Inimigo = choice(self._mostros)
                inimigo = Inimigo()
                combate(self.personagem, inimigo)
                if self.personagem.status['vida'] == 0:
                    return True
                elif self.personagem.status['vida'] > 0:
                    self.personagem.experiencia += inimigo.experiencia
                self.personagem.recuperar_magia_stamina()
            tela.limpar_tela2()
            return False

    def sortear_loot(self):
        if randint(0, 1):
            efeito_digitando('Loot encontrado.')
            sleep(1)
            Item = choice(vestes + armas)
            if issubclass(Item, Arma):
                item = Item(
                    dano = randint(1, 3), velo_ataque = randint(1, 2),
                    critico = randint(1, 3)
                )
            elif issubclass(Item, Roupa):
                item = Item(
                    armadura = randint(1, 3), velo_movi = randint(0, 3),
                    vida = randint(0, 3), resistencias = randint(1, 3)
                )
            elif issubclass(Item, Anel):
                item = Item(
                    nome = 'Anel', dano = randint(1, 3), vida = randint(1, 3),
                    resistencias = randint(1, 3), armadura = randint(1, 3)
                )
            self.personagem.pratas += randint(100, 300)
            self.personagem.inventario.append(item)

    def morto(self):
        self.personagem.ressucitar()
        tela.limpar_tela()
        tela.limpar_tela2()
        tela.imprimir('você foi morto e foi ressucitado.')
        sleep(3)
