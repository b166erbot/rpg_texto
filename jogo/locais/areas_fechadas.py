from itertools import chain
from random import choice, randint
from time import sleep

from jogo.assincrono.combate import combate
from jogo.personagens.monstros import (
    Arauto,
    Ceifador,
    DemonioDoCovil,
    Esqueleto,
    FilhoDoArauto,
    bosses_da_floresta,
    monstros_da_floresta,
)
from jogo.tela.imprimir import Imprimir, efeito_digitando

tela = Imprimir()


class Local:
    def __init__(self, local: str):
        self.local = local

    def __str__(self):
        return f"entrando em {self.local}"

    def __repr__(self):
        return f"local: {self.local}"


def gerar_local_linear(passagens: list[str], locais: list[str]):
    """Função que retorna uma lista com passagens."""
    passagens = list(map(Local, passagens))
    locais = list(map(Local, locais))
    fluxo = [choice(passagens) for _ in range(randint(2, 5))]
    passagem = choice(locais)
    fluxo.append(passagem)
    return fluxo


class Caverna:
    """Classe que constroi uma caverna com caminhos aleatórios."""

    def __init__(self, nome_caverna: str, personagem, level: int):
        self.nome = nome_caverna
        self.personagem = personagem
        passagens = [
            "bifurcação",
            "área aberta",
            "passagem estreita",
            "área com pedregulhos",
            "lago subterraneo",
            "área com estalagmites e estalactites",
        ]
        locais = [
            "local estreito e sem saída",
            "local sem saída",
            "cachoeira interna",
        ]
        self._caminhos = (
            gerar_local_linear(passagens, locais) for _ in range(3)
        )
        self._caminhos = chain(*self._caminhos)
        self._mostros = monstros_da_floresta
        self._locais_com_monstros = [
            "local estreito e sem saída",
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
        Boss = choice(bosses_da_floresta)
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
            self.personagem.experiencia.depositar_valor(boss.experiencia)
            boss.sortear_drops(self.personagem)
            boss.sortear_drops_quest(self.personagem)
        self.personagem.recuperar_magia_stamina_cem_porcento()

    def sortear_inimigos(self):
        """Método que sorteia os inimigos para o personagem."""
        if bool(randint(0, 1)):
            efeito_digitando("Monstros encontrados.")
            sleep(1)
            tela.limpar_tela()
            for y in range(randint(1, 3)):
                Inimigo = choice(self._mostros)
                inimigo = Inimigo(level=self.level)
                combate(self.personagem, inimigo)
                if self.personagem.status["vida"] == 0:
                    return True
                self.personagem.experiencia.depositar_valor(inimigo.experiencia)
                inimigo.sortear_drops(self.personagem)
                self.personagem.recuperar_magia_stamina_cem_porcento()
            return False

    def morto(self):
        """Método que ressucita o personagem e exibe na tela "morto"."""
        self.personagem.ressucitar()
        tela.imprimir("você foi morto e foi ressucitado.")
        sleep(3)


class CovilDoArauto:
    def __init__(self, personagem, level: int):
        self.nome = "Covil do Arauto"
        self.personagem = personagem
        passagens = [
            "bifurcação",
            "passagem estreita",
            "área a direita",
            "área a esquerda",
        ]
        locais = [
            "local sem saída",
            "área aberta",
        ]
        self._caminhos = (
            gerar_local_linear(passagens, locais) for _ in range(3)
        )
        self._caminhos = chain(*self._caminhos)
        self._mostros = [DemonioDoCovil, FilhoDoArauto]
        self._locais_com_monstros = [
            "local sem saída",
            "área aberta",
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
        boss = Arauto(self.level, status)
        tela.limpar_tela()
        tela.imprimir("Boss encontrado!\n", "vermelho")
        tela.imprimir("Chance de dropar item raro\n")
        tela.imprimir(str(boss) + "\n")
        lutar = self._lutar_ou_fugir()
        if lutar:
            combate(self.personagem, boss)
            if self.personagem.status["vida"] == 0:
                self.morto()
                return
            elif self.personagem.status["vida"] > 0:
                self.personagem.experiencia.depositar_valor(boss.experiencia)
                boss.sortear_drops(self.personagem)
                boss.sortear_drops_quest(self.personagem)
            self.personagem.recuperar_magia_stamina_cem_porcento()

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
                self.personagem.experiencia.depositar_valor(inimigo.experiencia)
                inimigo.sortear_drops(self.personagem)
                self.personagem.recuperar_magia_stamina_cem_porcento()
            return False

    def morto(self):
        """Método que ressucita o personagem e exibe na tela "morto"."""
        self.personagem.ressucitar()
        tela.imprimir("você foi morto e foi ressucitado.")
        sleep(3)

    def _lutar_ou_fugir(self):
        # esse método não limpa a tela, favor manter.
        tela.imprimir("Deseja lutar ou fugir?: ")
        resposta = tela.obter_string().lower()
        if resposta == "lutar":
            return True
        else:
            return False


class Catatumbas:
    def __init__(self, personagem, level: int):
        self.nome = "Catatumbas"
        self.personagem = personagem
        passagens = [
            "bifurcação",
            "tunel",
            "ala a direita",
            "ala a esquerda",
        ]
        locais = [
            "local sem saída",
            "área aberta",
        ]
        self._caminhos = (
            gerar_local_linear(passagens, locais) for _ in range(3)
        )
        self._caminhos = chain(*self._caminhos)
        self._mostros = [Esqueleto]
        self._locais_com_monstros = [
            "local sem saída",
            "área aberta",
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
        boss = Ceifador(self.level, status)
        tela.limpar_tela()
        tela.imprimir("Boss encontrado!\n", "vermelho")
        tela.imprimir("Chance de dropar item raro\n")
        tela.imprimir(str(boss) + "\n")
        lutar = self._lutar_ou_fugir()
        if lutar:
            combate(self.personagem, boss)
            if self.personagem.status["vida"] == 0:
                self.morto()
                return
            elif self.personagem.status["vida"] > 0:
                self.personagem.experiencia.depositar_valor(boss.experiencia)
                boss.sortear_drops(self.personagem)
                boss.sortear_drops_quest(self.personagem)
            self.personagem.recuperar_magia_stamina_cem_porcento()

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
                self.personagem.experiencia.depositar_valor(inimigo.experiencia)
                inimigo.sortear_drops(self.personagem)
                self.personagem.recuperar_magia_stamina_cem_porcento()
            return False

    def morto(self):
        """Método que ressucita o personagem e exibe na tela "morto"."""
        self.personagem.ressucitar()
        tela.imprimir("você foi morto e foi ressucitado.")
        sleep(3)

    def _lutar_ou_fugir(self):
        # esse método não limpa a tela, favor manter.
        tela.imprimir("Deseja lutar ou fugir?: ")
        resposta = tela.obter_string().lower()
        if resposta == "lutar":
            return True
        else:
            return False
