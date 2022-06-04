from jogo.tela.imprimir import formas, Imprimir
from jogo.locais.cavernas import Caverna
from jogo.personagens.npc import Comerciante
from jogo.locais.areas_abertas import Floresta
from time import sleep
from jogo.utils import chunk, salvar_jogo
import sys
from unittest.mock import MagicMock
from pathlib import Path
from jogo.personagens.npc import lorena, mercante


# Silenciar o pygame para não imprimir nada na tela
sys.stdout = MagicMock()
from pygame import mixer
sys.stdout = sys.__stdout__


mixer.init()
tela = Imprimir()


class Tela_principal:
    def __init__(self, personagem):
        self._texto = [
            'O que deseja fazer?',
            '1 - explorar uma floresta',
            '2 - visitar o comerciante',
            '3 - equipar equipamentos',
            '4 - desequipar equipamentos',
            '5 - mostrar equipamentos equipados',
            '6 - vender itens',
            '7 - mostrar seu dinheiro',
            '8 - mostrar sua experiência',
            '9 - mostrar o status',
            '10 - salvar jogo',
            '11 - deletar save',
            '12 - sair'
        ]
        self.personagem = personagem

    def ciclo(self):
        mixer.music.load('vilarejo.ogg')
        mixer.music.play()
        forma = f"{formas[227]} {{}} {formas[228]}"
        while True:
            tela.limpar_tela()
            for texto in self._texto:
                tela.imprimir(forma.format(texto) + '\n')
            tela.imprimir(': ')
            caracter = tela.obter_string()
            if not caracter or not caracter.isnumeric():
                continue
            caracter = int(caracter)
            if caracter == 1:
                mixer.music.stop()
                self.floresta()
                mixer.music.load('vilarejo.ogg')
                mixer.music.play()
            elif caracter == 2:
                mercante.interagir(self.personagem)
            elif caracter == 3:
                self.equipar_equipamentos()
            elif caracter == 4:
                self.desequipar()
            elif caracter == 5:
                tela.limpar_tela()
                equipamentos = self.personagem.equipamentos.values()
                for item in equipamentos:
                    tela.imprimir(f"{item}\n")
                sleep(4)
            elif caracter == 6:
                self.vender_item()
            elif caracter == 7:
                tela.imprimir(str(self.personagem.pratas))
                sleep(4)
            elif caracter == 8:
                tela.imprimir(f"{formas[230]} {self.personagem.experiencia}")
                sleep(4)
            elif caracter == 9:  # depois colocar o resto dos status aqui.
                p = self.personagem
                tela.imprimir(
                    f"{p.nome}: vida - {p.status['vida']}, armadura - "
                    f"{p.status['armadura']}, resistencias - "
                    f"{p.status['resis']}, dano - {p.status['dano']}"
                )
                sleep(4)
            elif caracter == 10:
                salvar_jogo(self.personagem, 'save.pk')
                tela.imprimir('jogo salvo')
                sleep(3)
            elif caracter == 11:
                arquivo = Path('save.pk')
                if arquivo.exists():
                    arquivo.unlink()
                    tela.imprimir('save deletado')
                else:
                    tela.imprimir('save não existente')
                sleep(3)
            elif caracter == 12:
                quit()

    def equipar_equipamentos(self):
        numero = self._obter_numero('deseja equipar qual equipamento: ')
        if bool(numero):
            inventario = dict(enumerate(self.personagem.inventario))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                self.personagem.equipar(equipamento)

    def vender_item(self):
        numero = self._obter_numero('deseja vender qual equipamento: ')
        if bool(numero):
            inventario = dict(enumerate(self.personagem.inventario))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                self.personagem.vender(equipamento)

    def desequipar(self):
        numero = self._obter_numero('deseja desequipar qual equipamento: ')
        if bool(numero):
            inventario = dict(enumerate(self.personagem.inventario))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                self.personagem.desequipar(equipamento)

    def floresta(self):
        tela.limpar_tela()
        nomes_florestas = [
            'amazonia', 'floresta rio preto', 'floresta do caçador',
            'floresta mata grande', 'floresta passo fundo',
            'floresta nublada', 'floresta negra'
        ]
        nomes_florestas_dict = dict(enumerate(nomes_florestas, 1))
        for numero, floresta in enumerate(nomes_florestas, 1):
            tela.imprimir(f"{numero} - {floresta}\n")
        tela.imprimir(': ')
        numero = tela.obter_string()
        if numero.isnumeric():
            mixer.music.load('som_da_floresta.ogg')
            mixer.music.play()
            numero = int(numero)
            floresta = nomes_florestas_dict[numero]
            floresta = Floresta(floresta, self.personagem, numero)
            floresta.explorar(lorena)
            self.personagem.recuperar_magia_stamina()
            self.personagem.status['vida'] = 100
            mixer.music.stop()

    def _obter_numero(self, mensagem):
        itens = list(enumerate(self.personagem.inventario))
        if len(itens) == 0:
            tela.imprimir('você não tem itens no inventario.')
            sleep(2)
            return ''
        itens = chunk(itens, 18)
        numeros_paginas = {f":{n}": n for n in range(1, len(itens) + 1)}
        numero = ':1'
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(itens)}"
                " - Para passar de página digite :numero exemplo-> :2\n"
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in itens[n -1]:
                mensagem2 = f"{numero} - {item}"
                if self.personagem.equipamentos.get(item.tipo) is item:
                    mensagem2 += ' *equipado*'
                tela.imprimir(mensagem2 + '\n')
            tela.imprimir(mensagem)
            numero = tela.obter_string()
        return numero


# TODO: restaurar a estamina/magia estando parado nos turnos.
# TODO: colocar mais cavernas
# TODO: colocar mais npcs com quests
# TODO: lutar ou fugir do boss?
# TODO: poções, venenos
# TODO: dragões
# TODO: combate entre personagens
