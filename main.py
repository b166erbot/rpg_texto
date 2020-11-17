"""
Modulo principal onde você cria a história.
Crie várias histórias, vivêncie e compartilhe sua experiência com outros
jogadores.
"""
import curses

curses.initscr()

from jogo.personagens.classes import Arqueiro, Guerreiro, Mago, Assassino
from jogo.personagens.npc import Comerciante
from jogo.locais.cavernas import Caverna
from jogo.tela.tela_principal import Tela_principal


def main():
    ### daqui para baixo é somente teste, nada oficial. ###
    # arqueiro = Arqueiro('argonian')
    # mago = Mago('high elf')
    # assassino = Assassino('khajiit')
    # personagens = [guerreiro, arqueiro, mago, assassino]
    guerreiro = Guerreiro('nord', True)
    tela = Tela_principal(guerreiro)
    tela.ciclo()
    # mercante = Comerciante('Farkas')
    # mercante.interagir(guerreiro)
    # Caverna('Caverna', guerreiro).explorar()



if __name__ == '__main__':
    try:
        main()
    finally:
        curses.endwin()


# TODO: botar pra cantar canções ao mesmo tempo que a letra ou ressitar uma lingua
# antiga ao mesmo tempo que o texto gerado na tela.
