"""
Modulo principal onde você cria a história.
Crie várias histórias, vivêncie e compartilhe sua experiência com outros
jogadores.
"""
import curses

curses.initscr()
curses.start_color()

from pathlib import Path
from time import sleep

from jogo.itens.pocoes import curas
from jogo.itens.vestes import Peitoral
from jogo.locais.cavernas import Caverna
from jogo.personagens.classes import (
    Arqueiro,
    Assassino,
    Clerigo,
    Guerreiro,
    Mago,
    Monge,
)
from jogo.personagens.npc import Banqueiro, Comerciante, Pessoa
from jogo.quests.quests import QuestStatus, quests_da_lorena
from jogo.tela.imprimir import Imprimir
from jogo.tela.menu import Menu
from jogo.utils import carregar_jogo


def main():
    tela = Imprimir()
    if Path("save.pkl").exists():
        personagem = carregar_jogo("personagem", "save.pkl")
        lorena = carregar_jogo("Lorena", "save.pkl")
        banqueiro = carregar_jogo("Tiago", "save.pkl")
        tela.imprimir("jogo carregado", "cyan")
        sleep(2)
    else:
        lorena = Pessoa("Lorena")
        quests_status = [
            QuestStatus(quest(lorena.nome)) for quest in quests_da_lorena
        ]
        lorena.receber_quest_status(quests_status)
        banqueiro = Banqueiro("Tiago")
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
    comerciante = Comerciante("farkas", curas)
    menu = Menu(personagem)
    menu.obter_npcs([lorena, comerciante, banqueiro])
    menu.ciclo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()
