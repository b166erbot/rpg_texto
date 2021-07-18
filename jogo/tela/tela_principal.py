from jogo.tela.imprimir import formas, Imprimir
from jogo.locais.cavernas import Caverna
from jogo.personagens.npc import Comerciante
from time import sleep
from jogo.utils import vender


tela = Imprimir()


class Tela_principal:
    def __init__(self, personagem):
        self._texto = [
            'O que deseja fazer?',
            '1 - explorar uma caverna',
            '2 - visitar o comerciante',
            '3 - equipar equipamentos',
            '4 - mostrar equipamentos equipados',
            '5 - mostrar seu dinheiro',
            '6 - vender itens',
            '7 - sair'
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
                for item in equipamentos:
                    tela.imprimir(f"{item}\n")
                sleep(4)
            elif caracter == 5:
                tela.imprimir(str(self.personagem.pratas))
                sleep(4)
            elif caracter == 6:
                self.vender_item()
            elif caracter == 7:
                quit()

    def editar_equipamentos(self):
        tela.limpar_tela()
        for numero, item in enumerate(self.personagem.inventario):
            tela.imprimir(f"{numero} - {item}\n")
        tela.imprimir('deseja equipar qual equipamento: ')
        numero = tela.obter_string()
        if numero.isnumeric():
            inventario = dict(enumerate(self.personagem.inventario))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                self.personagem.equipar(equipamento)

    def vender_item(self):
        tela.limpar_tela()
        for numero, item in enumerate(self.personagem.inventario):
            tela.imprimir(f"{numero} - {item}\n")
        tela.imprimir('deseja vender qual equipamento: ')
        numero = tela.obter_string()
        if numero.isnumeric():
            inventario = dict(enumerate(self.personagem.inventario))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                vender(equipamento, self.personagem)


# TODO: por os atributos dos itens no personagem
# TODO: troca de arma volta para o inventario a equipada.
# TODO: restaurar a estamina/magia estando parado nos turnos.
# TODO: caso os itens sejam vendidos, os mesmos devem ser removidos do inventario.
