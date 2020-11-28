from random import randint, choice
from time import sleep
from re import compile
from jogo.personagens.monstros import Cascudinho, Traquinagem, Topera_boss
from jogo.assincrono.combate import combate
from jogo.tela.imprimir import efeito_digitando, Imprimir
from jogo.itens.pocoes import curas
from jogo.itens.vestes import tudo


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

    def explorar(self):
        if self.verificar_requisitos():
            self._tela.limpar_tela()
            self._tela.imprimir(
                f'deseja explorar a caverna: {self.nome} s/n?\n'
            )
            if self._tela.obter_string().decode().lower() == 's':
                for x in self._caminho:
                    efeito_digitando(x)
                    if self._substituir('', x) in self._locais:
                        self.sortear_inimigos()
                        self.sortear_loot()
                        self._tela.limpar_tela()
                boss = Topera_boss(status = {
                    'vida': 200, 'dano': 5, 'resis': 15, 'velo-ataque': 1,
                    'critico':15, 'armadura': 15, 'magia': 100, 'stamina': 100,
                    'velo-movi': 1}
                )
                combate(self.personagem, boss)
                self._tela.limpar_tela()
                self._tela.limpar_tela2()
                if self.personagem.status['vida'] == 0:
                    quit()
            self.personagem.recuperar_magia_stamina()
            self.personagem.status['vida'] = 100

    def sortear_inimigos(self):
        if randint(0, 1):
            efeito_digitando('Monstros encontrados.')
            sleep(1)
            self._tela.limpar_tela()
            for y in range(randint(1, 3)):
                inimigo = choice(self._mostros)()
                combate(self.personagem, inimigo)
                if self.personagem.status['vida'] == 0:
                    quit()
                self.personagem.recuperar_magia_stamina()
            self._tela.limpar_tela2()

    def sortear_loot(self):
        if randint(0, 1):
            efeito_digitando('Loot encontrado.')
            sleep(1)
            item = choice(tudo)
            item_ = item(
                armadura = randint(1, 3), velo_movi = randint(0, 3),
                vida = randint(0, 3), resistencias = randint(1, 3)
            )
            self.personagem.inventario.append(item_)
            self._tela.imprimir('loot')

    def verificar_requisitos(self):
        pocoes = list(map(lambda x: x.nome, curas))
        quantidade = len(list(filter(
            lambda x: x.nome in pocoes,
            self.personagem.inventario
        )))
        if quantidade < 15:
            texto = ('garanta que você tenha ao menos 15 poções no inventário'
                     'para explorar essa caverna.')
            self._tela.imprimir(texto)
            return False
        return True
