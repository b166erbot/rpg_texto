from random import randint, choice
from readchar import readchar
from time import sleep
from re import compile
from jogo.excecoes import CavernaEnorme
from jogo.personagens.monstros import Cascudinho, Traquinagem
from jogo.assincrono.combate import combate
from jogo.decoradores import validador
from jogo.tela.imprimir import efeito_digitando, Imprimir, colorir


def local_linear(passagens, locais):
    fluxo = []
    for n in range(randint(2, 5)):
        passagem = colorir(choice(passagens), 'cyan')
        fluxo.append(f"entrando em {passagem}")
    passagem = colorir(choice(locais), 'amarelo')
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
        self._procurar = compile('\\x1b\[38;5;3m.*').search  # noqa

    # refatorar
    def explorar(self):
        if self.verificar_requisitos():
            print(f'deseja explorar a caverna: {self.nome} s/n?')
            if readchar().lower() == 's':
                for x in self._caminho:
                    efeito_digitando(x)
                    condicoes = all(
                        ('entrando' in x, self._procurar(x))
                    )
                    if condicoes:
                        self.sortear_inimigos()
                        self.sortear_loot()

    def sortear_inimigos(self):
        if randint(0, 1):
            efeito_digitando('Monstros encontrados.')
            sleep(1)
            self._tela.limpar_tela()
            for y in (1,):  # range(randint(1, 5))
                inimigo = choice(self._mostros)()
                combate(self.personagem, inimigo)
            self._tela.limpar_tela()

    def sortear_loot(self):
        if randint(0, 1):
            efeito_digitando('Loot encontrado.')
            sleep(1)
            for y in (1,):  # range(randint(0, 4))
                print(colorir('loot', 'amarelo'))  # temporário, adicionar loot depois

    def verificar_requisitos(self):
        item = next(filter(
            lambda x: x.nome == 'poção de vida fraca',
            self.personagem.inventario
        ))
        if not item or item.quantidade < 15:
            texto = ('garanta que você tenha ao menos 15 poções no inventário'
                     'para explorar essa caverna.')
            print(colorir(texto, 'vermelho'))
            return False
        return True
