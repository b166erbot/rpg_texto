from random import randint, choice
from readchar import readchar
from time import sleep
from re import compile
from jogo.excecoes import CavernaEnorme
from jogo.personagens.monstros import Cascudinho, Traquinagem
from jogo.assincrono.combate import combate
from jogo.decoradores import validador
from jogo.tela.imprimir import efeito_digitando, Imprimir


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
        'bifurcação', 'outra passagem', 'passagem estreita',
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


class Caverna:
    """ Classe que constroi uma caverna com caminhos aleatórios. """
    def __init__(self, nome_caverna: str, personagem):
        self.nome = nome_caverna
        self.personagem = personagem
        self._caminho = gerar_fluxo()
        self._mostros = [Cascudinho, Traquinagem]
        self._tela = Imprimir()
        self._locais = [
            'local estreito e sem saída', 'mineiração', 'local sem saída',
            'cachoeira interna'
        ]
        self._substituir = compile('entrando em ').sub  # noqa

    # refatorar
    def explorar(self):
        if self.verificar_requisitos():
            self._tela.limpar_tela()
            self._tela.imprimir(
                f'deseja explorar a caverna: {self.nome} s/n?\n'
            )
            if readchar().lower() == 's':
                for x in self._caminho:
                    efeito_digitando(x)
                    if self._substituir('', x) in self._locais:
                        self.sortear_inimigos()
                        self.sortear_loot()
                        self._tela.limpar_tela()

    def sortear_inimigos(self):
        if randint(0, 1):
            efeito_digitando('Monstros encontrados.')
            sleep(1)
            self._tela.limpar_tela()
            for y in range(randint(1, 3)):
                inimigo = choice(self._mostros)()
                combate(self.personagem, inimigo)
            self._tela.limpar_tela2()

    def sortear_loot(self):
        if randint(0, 1):
            efeito_digitando('Loot encontrado.')
            sleep(1)
            for y in (1,):  # range(randint(0, 4))
                self._tela.imprimir('loot')

    def verificar_requisitos(self):
        item = next(filter(
            lambda x: x.nome == 'poção de vida fraca',
            self.personagem.inventario
        ))
        if not item or item.quantidade < 15:
            texto = ('garanta que você tenha ao menos 15 poções no inventário'
                     'para explorar essa caverna.')
            self._tela.imprimir(texto)
            return False
        return True
