from asyncio import get_event_loop, wait
from typing import Tuple
from jogo.personagens.classes import (
    Arqueiro, Assassino, Guerreiro, Mago, Clerigo
)
from jogo.tela.imprimir import imprimir
from itertools import cycle, permutations


# class Combate:
#     """ Classe que cria todas as threads em um combate. """
#     def __init__(self, gerador: zip):
#         import pdb; pdb.set_trace()
#         self.threads = [Thread(target=x, args=y, daemon=True)
#                         for x, y in gerador]
#
#     def rodar(self):
#         for x in self.threads:
#             x.start()
#             x.join()


def combate(*personagens: Tuple[Arqueiro, Assassino, Guerreiro, Mago, Clerigo]):
    """
    Função que faz os combates entre personagens.

    Essa função faz com que todos os personagens passados se auto ataquem ao
    mesmo tempo. portanto, se for passado 3 personagens, so 3 irão se atacar.
    """

    # daqui pra baixo é só putaria e linkin park tocando..
    personagens = list(permutations(personagens, 2))
    ciclo = get_event_loop()
    ciclo2 = cycle(range(len(personagens)))
    tarefas = [ciclo.create_task(x.atacar(y, ciclo2)) for x, y in personagens]
    ciclo.run_until_complete(wait(tarefas))
    # ciclo.close()
