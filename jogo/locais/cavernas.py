from random import randint, choices, choice
from readchar import readchar
from jogo.excecoes.locais import CavernaEnorme
from jogo.personagens.classes import (
    Arqueiro, Guerreiro, Mago, Assassino, Clerigo
)
from jogo.assincrono.combate import combate
from typing import Generator
from time import sleep


def trava(func):
    def inner(*args):
        if args[1] > 15:
            raise CavernaEnorme('profundidade_maxima precisa ser menor que 16.')
        return func(*args)
    return inner


@trava
def gerar_fluxo(locais: list, profundidade_maxima: int, local: str) -> dict:
    dicio = {}
    rotas = ['bifurcação', 'outra passagem']
    if profundidade_maxima > 0:
        if local in rotas:
            dicio[local] = {
                'caminho1': gerar_fluxo(
                    locais, profundidade_maxima - 1,
                    choice(rotas if randint(0, 1) else locais)
                ),
                'caminho2': gerar_fluxo(
                    locais, profundidade_maxima - 1,
                    choice(rotas if randint(0, 1) else locais)
                )
            }
        else:
            dicio = choice(locais)
    else:
        dicio = choice(locais)
    return dicio


class Caverna:
    """ Classe que constroi uma caverna com caminhos aleatórios. """
    def __init__(self, nome_caverna: str, personagem):
        self.nome = nome_caverna
        self.personagem = personagem
        self._rotas = ['bifurcação' , 'outra passagem']
        self._locais = [
            'estreito e sem saída', 'mineiração', 'sem saída',
            'cachoeira interna'
        ]
        self._caminho = gerar_fluxo(self._locais, 4, choice(self._rotas))
        self._classes = [Arqueiro, Guerreiro, Mago, Assassino, Clerigo]

    # teste pra ver se está funcionando e depois crie os monstros.
    def explorar(self):
        print(f'deseja explorar a caverna: {self.nome} s/n?')
        if readchar().lower() == 's':
            caminhos = list(self.organizar_rotas(self._caminho))
            for x in caminhos:
                print(f'entrando em {x}')
                sleep(1)
                if all((x not in self._rotas, randint(0, 1))):
                    print('Monstros encontrados.')
                    sleep(1)
                    for y in (1,):  # range(randint(1, 5))
                        combate(choice(self._classes)('qualquer nome'),
                                self.personagem)
                print(f'saindo de {x}')
                sleep(1)


    def organizar_rotas(self, dicio: dict) -> Generator:
        """ Método que transforma um dicionário em um gerador. """
        if isinstance(dicio, dict):
            for x in dicio.keys():
                yield x
                yield from self.organizar_rotas(dicio[x])
        else:
            yield dicio
