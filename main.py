"""
Modulo principal onde você cria a história.
Crie várias histórias, vivêncie e compartilhe sua experiência com outros
jogadores.
"""

from jogo.personagens.classes import Arqueiro, Guerreiro, Mago, Assassino
from jogo.personagens.monstros import Cascudinho
from jogo.personagens.npc import Comerciante
from jogo.assincrono.combate import combate
from jogo.locais.cavernas import Caverna
from screen import cursor


def main():
    ### daqui para baixo é somente teste, nada oficial. ###
    ressucitar_todos = lambda personagens: [x.ressucitar() for x in personagens]  # remover
    arqueiro = Arqueiro('argonian')
    guerreiro = Guerreiro('nord')
    mago = Mago('high elf')
    assassino = Assassino('khajiit')
    personagens = [guerreiro, arqueiro, mago, assassino]
    # monstro = Cascudinho()
    # combate(guerreiro, monstro)
    # combate(guerreiro, arqueiro)
    # ressucitar_todos(personagens)
    # combate(guerreiro, mago)
    # combate(*personagens)
    print('para explorar uma caverna você precisa comprar no mínimo 15 poções.')
    farkas = Comerciante('Farkas')
    farkas.interagir(guerreiro)
    Caverna('local fictício', guerreiro).explorar()


if __name__ == '__main__':
    try:
        cursor.hide()
        main()
    finally:
        cursor.show()
