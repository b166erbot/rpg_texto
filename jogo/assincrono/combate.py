from asyncio import get_event_loop, wait
from typing import Tuple
from itertools import permutations
from jogo.tela.imprimir import Imprimir


tela = Imprimir()


def combate(*personagens: Tuple):
    """
    Função que faz os combates entre personagens.
    """

    # daqui pra baixo é só putaria e linkin park tocando..
    personagens = list(permutations(personagens, 2))
    ciclo = get_event_loop()
    tarefas = [ciclo.create_task(x.atacar(y)) for x, y in personagens]
    tela.limpar_tela()
    tela.imprimir('digite os números 1 e 2 para dar golpes no seu adversário.')
    ciclo.run_until_complete(wait(tarefas))
    tela.limpar_tela()
    # ciclo.close()
