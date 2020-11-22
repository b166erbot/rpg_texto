from jogo.tela.imprimir import formas, Imprimir
from jogo.locais.cavernas import Caverna
from jogo.personagens.npc import Comerciante
from time import sleep


class Tela_principal:
    tela = Imprimir()

    def __init__(self, personagem):
        self._texto = [
            'O que deseja fazer?',
            '1 - explorar uma caverna',
            '2 - visitar o comerciante',
            '3 - editar equipamentos',
            '4 - imprimir equipamentos',
            '5 - sair'
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
                self.editar_equipamentos()
            elif caracter == 4:
                equipamentos = self.personagem.equipamentos.values()
                arma = self.personagem.arma
                for item in equipamentos:
                    self.tela.imprimir(f"{item}\n")
                self.tela.imprimir(f"{arma}\n")
                sleep(4)
            elif caracter == 5:
                quit()

    def editar_equipamentos(self):
        self.tela.limpar_tela()
        for numero, item in enumerate(self.personagem.inventario):
            self.tela.imprimir(f"{numero} - {item}" + '\n')
        self.tela.imprimir('deseja usar qual equipamento: ')
        caracter = int(self.tela.obter_string())
        inventario = dict(enumerate(self.personagem.inventario))
        self.personagem.equipar(inventario[caracter])
