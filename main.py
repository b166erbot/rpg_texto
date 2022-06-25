"""
Modulo principal onde você cria a história.
Crie várias histórias, vivêncie e compartilhe sua experiência com outros
jogadores.
"""
import curses

curses.initscr()
curses.start_color()

curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

from pathlib import Path
from time import sleep

from jogo.itens.moedas import Draconica
from jogo.itens.pocoes import curas
from jogo.itens.quest import ItemQuest
from jogo.personagens.classes import (
    Arqueiro,
    Assassino,
    Clerigo,
    Guerreiro,
    Mago,
    Monge,
)
from jogo.personagens.npc import (
    Banqueiro,
    Comerciante,
    ComercianteItemQuest,
    Pessoa,
)
from jogo.quests import quests_da_lorena, quests_do_eivor
from jogo.save import carregar_jogo_tela, salvar_jogo
from jogo.tela.imprimir import Imprimir
from jogo.tela.menu import Menu

tela = Imprimir()


def novo_jogo_saves(nomes: list[str]):
    mensagens = {
        str(x): y for x, y in enumerate(["novo jogo", "carregar jogo"], 1)
    }
    resposta = ""
    while not resposta.isnumeric() and not resposta in mensagens:
        tela.limpar_tela()
        for numero, mensagem in mensagens.items():
            tela.imprimir(f"{numero} - {mensagem}\n", "cyan")
        tela.imprimir("Deseja qual opção: ", "cyan")
        resposta = tela.obter_string()
    resposta = mensagens[resposta]
    if resposta == "carregar jogo":
        personagens = carregar_jogo_tela(nomes)
        if bool(personagens):
            tela.imprimir("jogo carregado", "cyan")
            sleep(2)
            bram = ComercianteItemQuest(
                "Bram", [Draconica], [ItemQuest("Coração de Dragão")]
            )
            personagens_, nome_do_save = personagens
            personagens_ += (bram,)
            return (personagens_, nome_do_save)
        else:
            return False
    elif resposta == "novo jogo":
        lorena = Pessoa("Lorena")
        quests = [quest(lorena.nome) for quest in quests_da_lorena]
        lorena.receber_quest(quests)
        eivor = Pessoa("Eivor")
        quests = [quest(eivor.nome) for quest in quests_do_eivor]
        eivor.receber_quest(quests)
        tiago = Banqueiro("Tiago")
        bram = ComercianteItemQuest(
            "Bram", [Draconica], [ItemQuest("Coração de Dragão")]
        )
        personagem = novo_personagem()
        nome_jogo = ""
        arquivos = [arquivo.name for arquivo in Path().glob("*.pkl")]
        arquivos.append(".pkl")
        while not bool(nome_jogo) or nome_jogo + ".pkl" in arquivos:
            tela.limpar_tela()
            tela.imprimir("qual é o nome do seu save?: ", "cyan")
            nome_jogo = tela.obter_string()
            if nome_jogo + ".pkl" in arquivos:
                tela.imprimir("erro: nome do arquivo existente", "vermelho")
                sleep(3)
        npcs = [lorena, eivor, tiago]
        nome_jogo += ".pkl"
        salvar_jogo(personagem, npcs, nome_jogo)
        return ([personagem] + npcs + [bram], nome_jogo)


def novo_personagem():
    nome = ""
    while not bool(nome):
        tela.limpar_tela()
        tela.imprimir("qual é o nome do seu personagem?: ", "cyan")
        nome = tela.obter_string()
    classes = [Arqueiro, Guerreiro, Mago, Assassino, Clerigo, Monge]
    classes_nomes = [
        "Arqueiro",
        "Guerreiro",
        "Mago",
        "Assassino",
        "Clerigo",
        "Monge",
    ]
    classes_dict = dict(zip(classes_nomes, classes))
    # transformar os números do enumerate em string
    classes_dict2 = {str(x): y for x, y in enumerate(classes_nomes)}
    numero_personagem = ""
    while numero_personagem not in classes_dict2:
        tela.limpar_tela()
        for numero, classe in classes_dict2.items():
            tela.imprimir(f"{numero} - {classe}\n", "cyan")
        tela.imprimir("Escolha a classe do seu personagem: ", "cyan")
        numero_personagem = tela.obter_string()
    Classe = classes_dict[classes_dict2[numero_personagem]]
    personagem = Classe(nome, True)
    return personagem


def main():
    personagens_nome_jogo = ""
    while not bool(personagens_nome_jogo):
        personagens_nome_jogo = novo_jogo_saves(
            ["Personagem", "Lorena", "Eivor", "Tiago"]
        )
    personagens, nome_jogo = personagens_nome_jogo
    personagem, lorena, eivor, tiago, bram = personagens
    comerciante = Comerciante("farkas", curas)
    menu = Menu(personagem, nome_jogo)
    menu.obter_npcs([lorena, comerciante, tiago, eivor, bram])
    menu.ciclo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()
