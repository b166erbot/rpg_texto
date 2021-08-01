from random import randint, choice
from .cavernas import Local
from jogo.tela.imprimir import Imprimir, efeito_digitando
from jogo.locais.cavernas import Caverna
from jogo.personagens.npc import Pessoa
from jogo.personagens.monstros import (
    Tartaruga, Camaleao, Tamandua, Sapo, ArvoreDeku
)
from jogo.assincrono.combate import combate
from time import sleep


tela = Imprimir()


def local_linear(passagens):
    passagens = list(map(Local, passagens))
    fluxo = []
    for numero in range(randint(3, 5)):
        passagem = choice(passagens)
        fluxo.append(passagem)
    return fluxo


def gerar_fluxo():
    passagens = [
        'matagal', 'area florestada', 'rio', 'trilha', 'gruta', 'corrego'
    ]
    fluxo = (
        local_linear(passagens) + ['pessoa desconhecida']
        + local_linear(passagens) + ['caverna']
        + local_linear(passagens) + ['caverna', 'arvore deku']
    )
    return fluxo


class Floresta:
    def __init__(self, nome: str, personagem, nivel: int):
        self.nome = nome
        self.personagem = personagem
        self._caminhos = gerar_fluxo()
        self.nivel = nivel

    def explorar(self, pessoa: Pessoa):
        tela.limpar_tela()
        tela.imprimir(self.nome + '\n')
        for caminho in self._caminhos:
            self.caverna_pessoa(caminho, pessoa)
        tela.imprimir('voltando ao início da floresta\n')
        for caminho in self._caminhos[:0:-1]:
            self.caverna_pessoa(caminho, pessoa)

    def caverna_pessoa(self, caminho: Local, pessoa: Pessoa):
        # pessoa != personagem
        efeito_digitando(str(caminho))
        if str(caminho) == 'caverna':
            tela.imprimir('deseja entrar na caverna? s/n\n')
            if tela.obter_string().lower() in ['s', 'sim']:
                caverna = Caverna('poço azul', self.personagem, self.nivel)
                caverna.explorar()
                self.personagem.recuperar_magia_stamina()
                self.personagem.status['vida'] = 100
            tela.limpar_tela()
        elif str(caminho) == 'pessoa desconhecida':
            tela.imprimir('deseja interagir com pessoa desconhecida?: ')
            if tela.obter_string().lower() in ['s', 'sim']:
                pessoa.interagir(self.personagem)
            tela.limpar_tela()
        elif str(caminho) == 'arvore deku':
            status = {
                'vida': 300, 'dano': 5, 'resis': 15, 'velo-ataque': 1,
                'critico':15, 'armadura': 15, 'magia': 100, 'stamina': 100,
                'velo-movi': 1}
            boss = ArvoreDeku(self.nivel, status)
            combate(self.personagem, boss)
            if self.personagem.status['vida'] == 0:
                self.morto()
                return
            elif self.personagem.status['vida'] > 0:
                self.personagem.experiencia += boss.experiencia
                boss.dar_loot_boss(self.personagem)
        morte = self.sortear_inimigos()
        if morte:
            self.morto()
            return
        for quest in self.personagem.quests:
            condicoes = [
                randint(1, 5) == 1,
                quest.item not in self.personagem.inventario,
                not pessoa.missao_finalizada
            ]
            if all(condicoes):
                self.personagem.inventario.append(quest.item)
                tela.imprimir(f"item {quest.item.nome} adiquirido.\n")
                sleep(1)

    def sortear_inimigos(self):
        if randint(1, 5) == 1:
            efeito_digitando('Monstros encontrados.')
            sleep(1)
            tela.limpar_tela()
            for y in range(randint(1, 3)):
                Inimigo = choice([Tartaruga, Camaleao, Tamandua, Sapo])
                inimigo = Inimigo()
                combate(self.personagem, inimigo)
                if self.personagem.status['vida'] == 0:
                    return True
                elif self.personagem.status['vida'] > 0:
                    self.personagem.experiencia += inimigo.experiencia
                    inimigo.sortear_drops(self.personagem)
                self.personagem.recuperar_magia_stamina()
            tela.limpar_tela2()
            return False

    def morto(self):
        self.personagem.ressucitar()
        tela.limpar_tela()
        tela.limpar_tela2()
        tela.imprimir('você está morto e foi ressucitado.')
        sleep(3)
