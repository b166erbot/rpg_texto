from asyncio import get_event_loop, wait
from itertools import permutations

from jogo.tela.imprimir import Imprimir

tela = Imprimir()


def combate(personagem1, personagem2):
    """Função que faz os combates entre personagens."""

    # daqui pra baixo é só putaria e linkin park tocando...
    personagens = list(permutations([personagem1, personagem2], 2))
    # reduzir a porcentagem de armadura/resistencia com base no lvl do inimigo
    personagem1.atualizar_porcentagem_por_level(personagem2.level)
    personagem2.atualizar_porcentagem_por_level(personagem1.level)
    ciclo = get_event_loop()
    tarefas = [ciclo.create_task(x.atacar(y)) for x, y in personagens]
    tela.limpar_tela()
    tela.imprimir(
        "a primeira barra é de mana, a segunda de vida e a terceira é de stamina"
    )
    tela.imprimir(f"digite 1 para usar -> {personagem1.habilidades_nomes[0]}\n")
    tela.imprimir(
        f"e digite 2 para usar -> {personagem1.habilidades_nomes[1]}\n"
    )
    ciclo.run_until_complete(wait(tarefas))
    tela.limpar_tela()
    # retornar ao normal a porcentagem de armadura/resistencia
    personagem1.atualizar_porcentagem()
    personagem2.atualizar_porcentagem()
    # ciclo.close()
