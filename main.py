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


def main():
    ### daqui para baixo é somente teste, nada oficial. ###
    t = Imprimir()
    t.imprimir('qual é o nome do seu personagem?: ')
    nome = t.obter_string()
    t.limpar_tela()
    classes = [Arqueiro, Guerreiro, Mago, Assassino, Clerigo]
    classes_nomes = ['arqueiro', 'guerreiro', 'mago', 'assassino', 'clerigo']
    classes_dict = dict(zip(classes_nomes, classes))
    dicionario = dict(enumerate(classes_nomes))
    for numero, classe in dicionario.items():
        t.imprimir(f"{numero} - {classe}\n")
    t.imprimir('Escolha a classe do seu personagem: ')
    numero = int(t.obter_string())
    classe = classes_dict[dicionario[numero]]
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
