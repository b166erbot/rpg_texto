"""
Modulo principal onde você cria a história.
Crie várias histórias, vivêncie e compartilhe sua experiência com outros
jogadores.
"""
import curses

curses.initscr()

from jogo.personagens.classes import Arqueiro, Guerreiro, Mago, Assassino
from jogo.personagens.monstros import Cascudinho
from jogo.personagens.npc import Comerciante
from jogo.assincrono.combate import combate
from jogo.locais.cavernas import Caverna


def main():
    ### daqui para baixo é somente teste, nada oficial. ###
    ressucitar_todos = lambda personagens: [x.ressucitar() for x in personagens]  # remover
    arqueiro = Arqueiro('argonian')
    guerreiro = Guerreiro('nord', True)
    mago = Mago('high elf')
    assassino = Assassino('khajiit')
    personagens = [guerreiro, arqueiro, mago, assassino]
    # monstro = Cascudinho()
    # combate(guerreiro, monstro)
    # combate(guerreiro, arqueiro)
    # ressucitar_todos(personagens)
    # combate(guerreiro, mago)
    # combate(*personagens)
    mercante = Comerciante('Farkas')
    mercante.interagir(guerreiro)
    Caverna('local fictício', guerreiro).explorar()


if __name__ == '__main__':
    try:
        main()
    finally:
        curses.endwin()


# TODO: botar pra cantar canções ao mesmo tempo que a letra ou ressitar uma lingua
# antiga ao mesmo tempo que o texto gerado na tela.
