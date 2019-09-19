from random import randint, choices, choice
from readchar import readchar
from typing import Generator
from time import sleep
from re import compile
from jogo.excecoes import CavernaEnorme
from jogo.personagens.monstros import Cascudinho
from jogo.assincrono.combate import combate
from jogo.decoradores import validador
from jogo.anotacoes import Personagens
from jogo.tela.imprimir import efeito_digitando, Imprimir, colorir


texto = 'É necessário inserir uma profundidade máxima (<= 15) para essa função.'


# refatorar
@validador(lambda x: x[1] > 15, CavernaEnorme, texto)
def gerar_fluxo(locais: list, profundidade_maxima: int, local: str) -> list:
    rotas = ['bifurcação', 'outra_passagem']
    if profundidade_maxima > 0:
        if local in rotas:
            novo_local = lambda: choice(rotas if randint(0, 1) else locais)
            local = colorir(local, 'cyan')
            retorno = [
                f"entrando em {local}",
                *gerar_fluxo(locais, profundidade_maxima - 1, novo_local()),
                *gerar_fluxo(locais, profundidade_maxima - 1, novo_local()),
                f"saindo de {local}"
            ]
        else:
            local = colorir(local, 'amarelo')
            retorno = (f"entrando em {local}", f"saindo de {local}")
    else:  # como fazer para deletar esse else e continuar funcionando.
        local = colorir(local, 'cyan' if local in rotas else 'amarelo')
        retorno = (f"entrando em {local}", f"saindo de {local}")
    return retorno


class Caverna:
    """ Classe que constroi uma caverna com caminhos aleatórios. """
    def __init__(self, nome_caverna: str, personagem: Personagens):
        self.nome = nome_caverna
        self.personagem = personagem
        self._rotas = ['bifurcação' , 'outra_passagem']
        self._locais = [
            'local estreito e sem saída', 'mineiração', 'local sem saída',
            'cachoeira interna'
        ]
        self._caminho = gerar_fluxo(self._locais, 4, choice(self._rotas))
        self._mostros = [Cascudinho]
        self._tela = Imprimir()
        self._pegar_local = compile('(\w+ )?|(\\x1b\[(\d+;?)*m)|[ ]').sub

    # refatorar
    def explorar(self):
        if self.verificar_requisitos():
            print(f'deseja explorar a caverna: {self.nome} s/n?')
            if readchar().lower() == 's':
                for x in self._caminho:
                    efeito_digitando(x)
                    condicoes = all(
                        ('entrando' in x,
                        self._pegar_local('', x) not in self._rotas)
                    )
                    if condicoes:
                        self.sortear_inimigos_loot()

    def sortear_inimigos_loot(self):
        if randint(0, 1):
            efeito_digitando('Monstros encontrados.')
            sleep(1)
            self._tela.limpar_tela()
            for y in (1,):  # range(randint(1, 5))
                inimigo = choice(self._mostros)()
                combate(self.personagem, inimigo)
        if randint(0, 1):
            efeito_digitando('Loot encontrado.')
            sleep(1)
            for y in (1,):  # range(randint(0, 4))
                print(colorir('loot', 'amarelo'))  # temporário, adicionar loot depois

    def verificar_requisitos(self):
        item = self.personagem.inventario.get('poção de vida fraca')
        if not item or item.quantidade < 15:
            texto = ('garanta que você tenha ao menos 15 poções no inventário'
                     'para explorar essa caverna.')
            print(colorir(texto, 'vermelho'))
            return False
        return True
