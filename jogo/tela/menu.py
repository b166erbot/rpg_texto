import sys
from pathlib import Path
from time import sleep
from unittest.mock import MagicMock

from jogo.locais.areas_abertas import Floresta
from jogo.locais.cavernas import Caverna
from jogo.locais.habitaveis import Vilarejo
from jogo.personagens.npc import Comerciante, Pessoa
from jogo.quests.quests import QuestStatus, quests_da_lorena, ItemQuest
from jogo.tela.imprimir import Imprimir, formas
from jogo.utils import chunk, salvar_jogo

# Silenciar o pygame para não imprimir nada na tela
sys.stdout = MagicMock()
from pygame import mixer

sys.stdout = sys.__stdout__


mixer.init()
tela = Imprimir()


comerciante = Comerciante('farkas')

lorena = Pessoa('lorena')
quests_status = [
    QuestStatus(quest(lorena.nome)) for quest in quests_da_lorena
]
lorena.receber_quest_status(quests_status)


class Menu:
    def __init__(self, personagem):
        texto = ['O que deseja fazer?']
        texto2 = [
            'explorar uma floresta',
            'visitar o vilarejo',
            'equipar equipamentos',
            'desequipar equipamentos',
            'mostrar equipamentos equipados',
            'vender itens',
            'mostrar o status',
            'mostrar quests',
            'salvar jogo',
            'deletar save',
            'sair',
        ]
        self._texto = texto + [
            f"{numero} - {texto}" for numero, texto in enumerate(texto2, 1)
        ]
        self.personagem = personagem
        self.vilarejo = Vilarejo(
            'Vila dos hobbits', personagem, [lorena, comerciante]
        )
        self.personagem.inventario.append(ItemQuest('gatinho'))
        for _ in range(5):
            self.personagem.inventario.append(ItemQuest('galho'))

    def ciclo(self):
        """Método onde é exibido o menu principal para o usuário."""
        mixer.music.load('vilarejo.ogg')
        mixer.music.play()
        forma = f"{formas[227]} {{}} {formas[228]}"
        while True:
            tela.limpar_tela()
            for texto in self._texto:
                tela.imprimir(forma.format(texto) + '\n', 'cyan')
            tela.imprimir(': ')
            caracter = tela.obter_string()
            if not caracter.isnumeric():
                continue
            caracter = int(caracter)
            match caracter:
                case 1:
                    mixer.music.stop()
                    self.floresta()
                    mixer.music.load('vilarejo.ogg')
                    mixer.music.play()
                case 2:
                    self.vilarejo.explorar()
                case 3:
                    self.equipar_equipamentos()
                case 4:
                    self.desequipar()
                case 5:
                    tela.limpar_tela()
                    equipamentos = self.personagem.equipamentos.items()
                    for nome, item in equipamentos:
                        frase_negativa = f"Não há item equipado em {nome}\n"
                        frase_positiva = f"{nome}: {item}\n"
                        tela.imprimir(
                            frase_positiva if bool(item) else frase_negativa
                        )
                    tela.imprimir(
                        'aperte enter para retornar ao menu principal: '
                    )
                    tela.obter_string()
                case 6:
                    self.vender_item()
                case 7:
                    tela.limpar_tela()
                    p = self.personagem
                    tela.imprimir(
                        f"{p.nome} [{p.classe}]: vida - "
                        f"{p.status['vida']}, armadura - "
                        f"{p.status['armadura']}, resistencias - "
                        f"{p.status['resis']}, dano - {p.status['dano']}, "
                        f"dinheiro - {str(p.pratas)}, xp - {p.experiencia}, "
                        f"level - {p.level}\n",
                        'cyan'
                    )
                    tela.imprimir(
                        'aperte enter para retornar ao menu principal: ', 'cyan'
                    )
                    tela.obter_string()
                case 8:
                    self._obter_numero_quests()
                case 9:
                    salvar_jogo(self.personagem, 'save.pk')
                    tela.imprimir('jogo salvo', 'cyan')
                    sleep(3)
                case 10:
                    arquivo = Path('save.pk')
                    if arquivo.exists():
                        arquivo.unlink()
                        tela.imprimir('save deletado', 'cyan')
                    else:
                        tela.imprimir('save não existente', 'cyan')
                    sleep(3)
                case 11:
                    quit()

    def equipar_equipamentos(self):
        """Método que equipa equipamentos do inventário do personagem."""
        numero = self._obter_numero_equipamentos(
            'deseja equipar qual equipamento: '
        )
        if bool(numero):
            inventario = dict(enumerate(self.personagem.inventario))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                self.personagem.equipar(equipamento)

    def vender_item(self):
        """Método que vende um item do inventário do personagem."""
        numero = self._obter_numero_equipamentos(
            'deseja vender qual equipamento: '
        )
        if bool(numero):
            inventario = dict(enumerate(self.personagem.inventario))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                if not isinstance(equipamento, ItemQuest):
                    self.personagem.desequipar(equipamento)
                    self.personagem.vender(equipamento)

    def desequipar(self):
        """Método que desequipa um equipamento do personagem."""
        numero = self._obter_numero_equipamentos(
            'deseja desequipar qual equipamento: '
        )
        if bool(numero):
            inventario = dict(enumerate(self.personagem.inventario))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                self.personagem.desequipar(equipamento)

    def floresta(self):
        """Método que conduz o personagem à floresta."""
        tela.limpar_tela()
        nomes_florestas = [
            'amazonia', 'floresta rio preto', 'floresta do caçador',
            'floresta mata grande', 'floresta passo fundo',
            'floresta nublada', 'floresta negra'
        ]
        nomes_florestas_dict = dict(enumerate(nomes_florestas, 1))
        for numero, floresta in enumerate(nomes_florestas, 1):
            tela.imprimir(
                f"{numero} - {floresta} [nível da floresta: {numero}]\n"
            )
        tela.imprimir(': ')
        numero = tela.obter_string()
        if numero.isnumeric() and int(numero) in nomes_florestas_dict:
            mixer.music.load('som_da_floresta.ogg')
            mixer.music.play()
            numero = int(numero)
            floresta = nomes_florestas_dict[int(numero)]
            floresta = Floresta(floresta, self.personagem, numero)
            floresta.explorar(lorena)
            self.personagem.recuperar_magia_stamina()
            self.personagem.ressucitar()
            mixer.music.stop()

    def _obter_numero_equipamentos(self, mensagem):
        """Método que organiza as páginas para o usuário e retorna um número."""
        itens = list(enumerate(self.personagem.inventario))
        if len(itens) == 0:
            tela.imprimir('você não tem itens no inventario.', 'cyan')
            sleep(2)
            return ''
        itens = chunk(itens, 18)
        numeros_paginas = {f":{n}": n for n in range(1, len(itens) + 1)}
        numero = ':1'
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(itens)}"
                " - Para passar de página digite :numero exemplo-> :2\n", 'cyan'
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in itens[n -1]:
                mensagem2 = f"{numero} - {item}"
                if self.personagem.equipamentos.get(item.tipo) is item:
                    mensagem2 += ' *equipado*'
                tela.imprimir(mensagem2 + '\n')
            tela.imprimir(mensagem, 'cyan')
            numero = tela.obter_string()
        return numero

    def _obter_numero_quests(self):
        quests = list(enumerate(self.personagem.quests))
        if len(quests) == 0:
            tela.imprimir('você não tem quests.', 'cyan')
            sleep(2)
            return
        quests = chunk(quests, 17)
        numeros_paginas = {f":{n}": n for n in range(1, len(quests) + 1)}
        numero = ':1'
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(quests)}"
                " - Para passar de página digite :numero exemplo-> :2\n", 'cyan'
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in quests[n -1]:
                tela.imprimir(f"{numero} - {item}\n")
            tela.imprimir('aperte enter para retornar ao menu: ', 'cyan')
            numero = tela.obter_string()

# TODO: restaurar a estamina/magia estando parado nos turnos.
# TODO: colocar mais npcs com quests.
# TODO: lutar ou fugir do boss?
# TODO: poções, venenos.
# TODO: dragões.
# TODO: combate entre personagens bots.
# TODO: colocar o nome dos ataques tanto dos inimigos tanto do personagem na tela.
# TODO: e com o level, colocar subclasses aos personagens.
# TODO: fazer uma função que imprime a história do jogo.
# TODO: colocar tempo para ir até o vilarejo ou floresta.
# TODO: mostrar a classe do item para que a pessoa possa
# equipar de acordo com a classe (não dá, muito texto).
# TODO: luvas de ferro estão como luvas e já tem luvas no personagem.
# TODO: obsessão por primitivos na classe Humano
# TODO: resolver "não há item no peitoral"
# TODO: fazer as quests terem itens ao invéz de item
# TODO: fazer as quests aparecerem dependendo do lvl
