from asyncio import get_event_loop, wait
from typing import Tuple
from itertools import permutations
from jogo.personagens.classes import (
    Arqueiro, Assassino, Guerreiro, Mago, Clerigo
)
from jogo.tela.imprimir import Imprimir
from jogo.excecoes import QuantidadeDiferente
from jogo.decoradores import validador


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

texto = 'É necessário inserir exatamente 2 personagens para esta função'

@validador(lambda x: len(x) != 2, QuantidadeDiferente, texto)
def combate(*personagens: Tuple[Arqueiro, Assassino, Guerreiro, Mago, Clerigo]):
    """
    Função que faz os combates entre personagens.
    """

    # daqui pra baixo é só putaria e linkin park tocando..
    personagens = list(permutations(personagens, 2))
    temp = Imprimir()
    temp.gerar_ciclo(len(personagens))
    ciclo = get_event_loop()
    tarefas = [ciclo.create_task(x.atacar(y)) for x, y in personagens]
    ciclo.run_until_complete(wait(tarefas))
    # ciclo.close()
