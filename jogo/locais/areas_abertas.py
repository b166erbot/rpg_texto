from random import randint, choice
from .cavernas import Local
from jogo.tela.imprimir import Imprimir, efeito_digitando
from jogo.locais.cavernas import Caverna
from jogo.personagens.npc import Pessoa, funcao_quest, Quest
from jogo.itens.quest import ItemQuest
from jogo.personagens.monstros import (
    Tartaruga, Camaleao, Tamandua, Sapo
)
from jogo.assincrono.combate import combate
from time import sleep


tela = Imprimir()


def local_linear(passagens, locais):
    passagens = list(map(Local, passagens))
    fluxo = []
    for numero in range(randint(3, 5)):
        passagem = choice(passagens)
        fluxo.append(passagem)
    passagem = choice(locais)
    fluxo.append(passagem)
    return fluxo


def gerar_fluxo():
    passagens = [
        'matagal', 'area florestada', 'rio', 'trilha', 'gruta', 'corrego'
    ]
    locais = [
        'caverna', 'pessoa desconhecida'
    ]
    fluxo = (
        local_linear(passagens, locais) + local_linear(passagens, locais)
        + local_linear(passagens, locais)
    )
    return fluxo


class Floresta:
    def __init__(self, nome: str, personagem):
        self.nome = nome
        self.personagem = personagem
        self._caminhos = gerar_fluxo()

    def explorar(self):
        tela.limpar_tela()
        item = ItemQuest('gatinho')
        pessoa = Pessoa(
            'lorena', Quest('pegar o gatinho', 150, item),
            item, funcao_quest
        )
        tela.imprimir(self.nome + '\n')
        for caminho in self._caminhos:
            self.caverna_pessoa(caminho, pessoa)
        tela.imprimir('voltando ao início da floresta\n')
        for caminho in self._caminhos[::-1][:-1]:
            self.caverna_pessoa(caminho, pessoa)
        self.personagem.recuperar_magia_stamina()
        self.personagem.status['vida'] = 100

    def caverna_pessoa(self, caminho, pessoa):  # pessoa != personagem
        efeito_digitando(str(caminho))
        if str(caminho) == 'caverna':
            tela.imprimir('deseja entrar na caverna? s/n\n')
            if tela.obter_string().lower() in ['s', 'sim']:
                caverna = Caverna('poço azul', self.personagem)
                caverna.explorar()
            tela.limpar_tela()
        elif str(caminho) == 'pessoa desconhecida':
            tela.imprimir('deseja interagir com pessoa desconhecida?: ')
            if tela.obter_string().lower() in ['s', 'sim']:
                pessoa.interagir(self.personagem)
            tela.limpar_tela()
        morte = self.sortear_inimigos()
        for quest in self.personagem.quests:
            condicoes = [
                randint(1, 3) == 1,
                quest.item not in self.personagem.inventario,
                not pessoa.missao_finalizada
            ]
            if all(condicoes):
                self.personagem.inventario.append(quest.item)
                tela.imprimir(f"item {quest.item.nome} adiquirido.\n")
                sleep(1)
        if morte:
            self.morto()
            return

    def sortear_inimigos(self):
        if randint(1, 8) == 1:
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
                self.personagem.recuperar_magia_stamina()
            tela.limpar_tela2()
            return False

    def morto(self):
        self.personagem.ressucitar()
        tela.limpar_tela()
        tela.limpar_tela2()
        tela.imprimir('você está morto e foi ressucitado.')
        sleep(3)
