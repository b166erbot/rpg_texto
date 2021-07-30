"""
Modulo principal onde você cria a história.
Crie várias histórias, vivêncie e compartilhe sua experiência com outros
jogadores.
"""
import curses

curses.initscr()

from jogo.personagens.classes import (
    Arqueiro, Guerreiro, Mago, Assassino, Clerigo
)
from jogo.personagens.npc import Comerciante
from jogo.locais.cavernas import Caverna
from jogo.tela.tela_principal import Tela_principal
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
        tela.imprimir('qual é o nome do seu personagem?: ')
        nome = tela.obter_string()
        tela.limpar_tela()
        classes = [Arqueiro, Guerreiro, Mago, Assassino, Clerigo]
        classes_nomes = ['Arqueiro', 'Guerreiro', 'Mago', 'Assassino', 'Clerigo']
        classes_dict = dict(zip(classes_nomes, classes))
        classes_dict2 = dict(enumerate(classes_nomes))
        for numero, classe in classes_dict2.items():
            tela.imprimir(f"{numero} - {classe}\n")
        tela.imprimir('Escolha a classe do seu personagem: ')
        numero = int(tela.obter_string())
        classe = classes_dict[classes_dict2[numero]]
        personagem = classe(nome, True)
    tela = Tela_principal(personagem)
    tela.ciclo()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()
