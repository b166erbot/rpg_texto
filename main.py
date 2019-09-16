"""
Modulo principal onde você cria a história.
Crie várias histórias, vivêncie e compartilhe sua experiência com outros
jogadores.
"""

from jogo.personagens.classes import Arqueiro, Guerreiro, Mago, Assassino
from jogo.assincrono.combate import combate
from jogo.locais.cavernas import Caverna
from screen import cursor


def main():
    ### daqui para baixo é somente teste, nada oficial. afinal, falta muito ###
    ressucitar_todos = lambda personagens: [x.ressucitar() for x in personagens]  # remover
    cursor.hide()
    arqueiro = Arqueiro('argonian')
    guerreiro = Guerreiro('nord')
    mago = Mago('high elf')
    assassino = Assassino('khajiit')
    personagens = [guerreiro, arqueiro, mago, assassino]
    # combate(guerreiro, arqueiro)
    # ressucitar_todos(personagens)
    # combate(guerreiro, mago)
    # ressucitar_todos(personagens)
    # combate(mago, arqueiro)
    # ressucitar_todos(personagens)
    # combate(assassino, mago)
    # ressucitar_todos(personagens)
    # combate(assassino, guerreiro)
    # ressucitar_todos(personagens)
    # combate(assassino, arqueiro)
    # ressucitar_todos(personagens)
    # combate(*personagens)
    Caverna('local fictício', guerreiro).explorar()
    cursor.show()


if __name__ == '__main__':
    main()
