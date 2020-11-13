from asyncio import get_event_loop, wait
from typing import Tuple
from itertools import permutations
from jogo.excecoes import QuantidadeDiferente
from jogo.decoradores import validador


texto = 'É necessário inserir exatamente 2 personagens para esta função'


@validador(lambda x: len(x) != 2, QuantidadeDiferente, texto)
def combate(*personagens: Tuple):
    """
    Função que faz os combates entre personagens.
    """

    # daqui pra baixo é só putaria e linkin park tocando..
    personagens = list(permutations(personagens, 2))
    ciclo = get_event_loop()
    tarefas = [ciclo.create_task(x.atacar(y)) for x, y in personagens]
    ciclo.run_until_complete(wait(tarefas))
    # ciclo.close()
