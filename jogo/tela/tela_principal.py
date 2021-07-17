from jogo.tela.imprimir import formas, Imprimir
from jogo.locais.cavernas import Caverna
from jogo.personagens.npc import Comerciante
from time import sleep
from jogo.utils import equipar


tela = Imprimir()


class Tela_principal:
    def __init__(self, personagem):
        self._texto = [
            'O que deseja fazer?',
            '1 - explorar uma caverna',
            '2 - visitar o comerciante',
            '3 - editar equipamentos',
            '4 - mostrar equipamentos equipados',
            '5 - mostrar seu dinheiro',
            '6 - sair'
        ]
        self.personagem = personagem

    def ciclo(self):
        forma = f"{formas[227]} {{}} {formas[228]}"
        while True:
            tela.limpar_tela()
            for texto in self._texto:
                tela.imprimir(forma.format(texto) + '\n')
            tela.imprimir(': ')
            caracter = int(tela.obter_string())
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
                    tela.imprimir(f"{item}\n")
                tela.imprimir(f"{arma}\n")
                sleep(4)
            elif caracter == 5:
                tela.imprimir(str(self.personagem.pratas))
                sleep(4)
            elif caracter == 6:
                quit()

    def editar_equipamentos(self):
        tela.limpar_tela()
        for numero, item in enumerate(self.personagem.inventario):
            tela.imprimir(f"{numero} - {item}" + '\n')
        tela.imprimir('deseja equipar qual equipamento: ')
        numero = tela.obter_string()
        if numero.isnumeric():
            inventario = dict(enumerate(self.personagem.inventario))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                equipar(equipamento, self.personagem)


# TODO: colocar dinheiro nas recompensas
# TODO: vender itens
# TODO: por os atributos dos itens no personagem
