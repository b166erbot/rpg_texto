"""
Modulo principal onde você cria a história.
Crie várias histórias, vivêncie e compartilhe sua experiência com outros
jogadores.
"""
import curses

curses.initscr()

from jogo.personagens.classes import (
    Arqueiro, Guerreiro, Mago, Assassino, Clerigo, Monge
)
from jogo.personagens.npc import Comerciante
from jogo.locais.cavernas import Caverna
from jogo.tela.menu import Menu
from jogo.tela.imprimir import Imprimir
from jogo.utils import carregar_jogo
from pathlib import Path
from time import sleep


def main():
    tela = Imprimir()
    if Path('save.pk').exists():
        personagem = carregar_jogo('save.pk')
        tela.imprimir('jogo carregado')
        sleep(3)
    else:
        nome = ''
        while not bool(nome):
            tela.limpar_tela()
            tela.imprimir('qual é o nome do seu personagem?: ')
            nome = tela.obter_string()
        classes = [Arqueiro, Guerreiro, Mago, Assassino, Clerigo, Monge]
        classes_nomes = [
            'Arqueiro', 'Guerreiro', 'Mago', 'Assassino', 'Clerigo', 'Monge'
        ]
        classes_dict = dict(zip(classes_nomes, classes))
        classes_dict2 = dict(enumerate(classes_nomes))
        numero_personagem = ''
        while numero_personagem not in classes_dict2:
            tela.limpar_tela()
            for numero, classe in classes_dict2.items():
                tela.imprimir(f"{numero} - {classe}\n")
            tela.imprimir('Escolha a classe do seu personagem: ')
            numero_personagem = int(tela.obter_string())
        Classe = classes_dict[classes_dict2[numero_personagem]]
        personagem = Classe(nome, True)
    tela = Menu(personagem)
    tela.ciclo()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()
