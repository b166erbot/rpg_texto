import shelve
from pathlib import Path
from time import sleep

from jogo.tela.imprimir import Imprimir

tela = Imprimir()


def _salvar_jogo(nome_do_objeto: str, objeto, nome_do_arquivo: str):
    save = shelve.open(nome_do_arquivo)
    save[nome_do_objeto] = objeto


def _carregar_jogo(nome_do_objeto, nome_do_arquivo: str):
    save = shelve.open(nome_do_arquivo)
    return save[nome_do_objeto]


def carregar_jogo_tela(nomes: list[str]):
    arquivos = {
        str(x): y
        for x, y in enumerate(
            [arquivo.name for arquivo in Path().glob("*.pkl")], 1
        )
    }
    if len(arquivos) == 0:
        tela.imprimir("Não há saves para carregar.", "cyan")
        sleep(3)
        return
    resposta = ""
    while not resposta.isnumeric() or resposta not in arquivos:
        tela.limpar_tela()
        for numero, arquivo in arquivos.items():
            tela.imprimir(f"{numero} - {arquivo[:-4]}\n", "cyan")
        tela.imprimir("Deseja carregar qual jogo?: ", "cyan")
        resposta = tela.obter_string()
    return (
        [_carregar_jogo(nome, arquivos[resposta]) for nome in nomes],
        arquivos[resposta],
    )


def salvar_jogo(personagem, npcs, nome_jogo):
    # tem que salvar com o nome de personagem pois fica fácil de recuperar com esse nome
    _salvar_jogo("Personagem", personagem, nome_jogo)
    for npc in npcs:
        _salvar_jogo(npc.nome, npc, nome_jogo)
