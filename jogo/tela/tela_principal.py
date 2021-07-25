from jogo.tela.imprimir import formas, Imprimir
from jogo.locais.cavernas import Caverna
from jogo.personagens.npc import Comerciante
from jogo.locais.areas_abertas import Floresta
from time import sleep
from jogo.itens.quest import ItemQuest
from jogo.personagens.npc import Pessoa, Quest
from jogo.quests.funcoes_quests import funcao_quest


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
            '10 - sair'
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
                self.floresta()
            elif caracter == 2:
                mercante = Comerciante('farkas')
                mercante.interagir(self.personagem)
            elif caracter == 3:
                self.editar_equipamentos()
            elif caracter == 4:
                self.desequipar()
            elif caracter == 5:
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
                self.personagem.vender(equipamento)

    def desequipar(self):
        tela.limpar_tela()
        for numero, item in enumerate(self.personagem.inventario):
            tela.imprimir(f"{numero} - {item}\n")
        tela.imprimir('deseja desequipar qual equipamento: ')
        numero = tela.obter_string()
        if numero.isnumeric():
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
            numero = int(numero)
            floresta = nomes_florestas_dict[numero]
            item = ItemQuest('gatinho')
            pessoa = Pessoa(
                'lorena', Quest('pegar o gatinho', 150, 2000, item),
                item, funcao_quest
            )
            floresta = Floresta(floresta, self.personagem, numero)
            floresta.explorar(pessoa)
            self.personagem.recuperar_magia_stamina()
            self.personagem.status['vida'] = 100


# TODO: restaurar a estamina/magia estando parado nos turnos.
# TODO: colocar mais cavernas
# TODO: colocar mais npcs com quests
# TODO: lutar ou fugir
# TODO: imprimir quais botões digitar na batalha
# TODO: bosses dão itens melhorados
