from random import choice, randint
from time import sleep

from jogo.assincrono.combate import combate
from jogo.itens.pocoes import curas
from jogo.itens.vestes import Anel, Roupa
from jogo.itens.vestes import tudo as vestes
from jogo.personagens.monstros import bosses_comuns, monstros_comuns
from jogo.tela.imprimir import Imprimir, efeito_digitando

tela = Imprimir()


class Local:
    def __init__(self, local: str):
        self.local = local

    def __str__(self):
        return f"entrando em {self.local}"

    def __repr__(self):
        return f"local: {self.local}"


def local_linear(passagens: list[str], locais: list[str]):
    """Função que retorna uma lista com passagens."""
    passagens = list(map(Local, passagens))
    locais = list(map(Local, locais))
    fluxo = [choice(passagens) for _ in range(randint(2, 5))]
    passagem = choice(locais)
    fluxo.append(passagem)
    return fluxo


def gerar_fluxo():
    """Função que retorna uma lista com fluxos."""
    passagens = [
        "bifurcação",
        "área aberta",
        "passagem estreita",
        "área com pedregulhos",
        "lago subterraneo",
    ]
    locais = [
        "local estreito e sem saída",
        "mineiração",
        "local sem saída",
        "cachoeira interna",
    ]
    fluxo = (
        local_linear(passagens, locais)
        + local_linear(passagens, locais)
        + local_linear(passagens, locais)
    )
    return fluxo


class Caverna:
    """Classe que constroi uma caverna com caminhos aleatórios."""

    def __init__(self, nome_caverna: str, personagem, level: int):
        self.nome = nome_caverna
        self.personagem = personagem
        self._caminhos = gerar_fluxo()
        self._mostros = monstros_comuns
        self._locais_com_monstros = [
            "local estreito e sem saída",
            "mineiração",
            "local sem saída",
            "cachoeira interna",
        ]
        self.level = level

    def explorar(self):
        """Método que explora uma caverna com o personagem."""
        tela.limpar_tela()
        for caminho in self._caminhos:
            efeito_digitando(str(caminho))
            if caminho.local in self._locais_com_monstros:
                morto = self.sortear_inimigos()
                if morto:
                    self.morto()
                    return
                tela.limpar_tela()
        Boss = choice(bosses_comuns)
        status = {
            "vida": 300,
            "dano": 5,
            "resistencia": 15,
            "velo-ataque": 1,
            "critico": 15,
            "armadura": 15,
            "magia": 100,
            "stamina": 100,
            "velo-movi": 1,
        }
        boss = Boss(self.level, status)
        combate(self.personagem, boss)
        if self.personagem.status["vida"] == 0:
            self.morto()
            return
        elif self.personagem.status["vida"] > 0:
            self.personagem.experiencia.depositar_experiencia(boss.experiencia)
            boss.sortear_drops(self.personagem)
        self.personagem.recuperar_magia_stamina_cem_porcento()
        tela.limpar_tela()
        tela.limpar_tela2()

    def sortear_inimigos(self):
        """Método que sorteia os inimigos para o personagem."""
        if randint(0, 1):
            efeito_digitando("Monstros encontrados.")
            sleep(1)
            tela.limpar_tela()
            for y in range(randint(1, 3)):
                Inimigo = choice(self._mostros)
                inimigo = Inimigo(level=self.level)
                combate(self.personagem, inimigo)
                if self.personagem.status["vida"] == 0:
                    return True
                self.personagem.experiencia.depositar_experiencia(
                    inimigo.experiencia
                )
                inimigo.sortear_drops(self.personagem)
                self.personagem.recuperar_magia_stamina()
            tela.limpar_tela2()
            return False

    def morto(self):
        """Método que ressucita o personagem e exibe na tela "morto"."""
        self.personagem.ressucitar()
        tela.limpar_tela()
        tela.limpar_tela2()
        tela.imprimir("você foi morto e foi ressucitado.")
        sleep(3)
