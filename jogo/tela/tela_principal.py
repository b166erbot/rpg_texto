# 227 228

from jogo.tela.imprimir import formas, Imprimir
from jogo.locais.cavernas import Caverna
from jogo.personagens.npc import Comerciante


class Tela_principal:
    tela = Imprimir()

    def __init__(self, personagem):
        self._texto = [
            'O que deseja fazer?',
            '1 - explorar uma caverna',
            '2 - visitar o comerciante',
            '3 - sair'
        ]
        self.personagem = personagem

    def ciclo(self):
        forma = f"{formas[227]} {{}} {formas[228]}"
        while True:
            self.tela.limpar_tela()
            for texto in self._texto:
                self.tela.imprimir(forma.format(texto) + '\n')
            self.tela.imprimir(': ')
            caracter = int(self.tela.obter_string())
            if caracter == 1:
                caverna = Caverna('caverna', self.personagem)
                caverna.explorar()
            elif caracter == 2:
                mercante = Comerciante('farkas')
                mercante.interagir(self.personagem)
            elif caracter == 3:
                quit()
