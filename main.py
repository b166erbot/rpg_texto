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
    dicionario = dict(enumerate(classes))
    for numero, classe in dicionario.items():
        t.imprimir(f"{numero} - {classe}\n")
    t.imprimir('Escolha a classe do seu personagem: ')
    numero = int(t.obter_string())
    classe = dicionario[numero]
    personagem = classe(nome, True)
    tela = Tela_principal(personagem)
    tela.ciclo()



if __name__ == '__main__':
    try:
        main()
    finally:
        curses.endwin()


# TODO: botar pra cantar canções ao mesmo tempo que a letra ou ressitar uma lingua
# antiga ao mesmo tempo que o texto gerado na tela.
