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
from jogo.itens.vestes import roupas_draconicas
from jogo.personagens.classes import (
    Arqueiro,
    Assassino,
    Clerigo,
    Guerreiro,
    Mago,
    Monge,
    Druida,
)
from jogo.personagens.npc import (
    Banqueiro,
    Comerciante,
    ComercianteItemQuest,
    Ferreiro,
    Pessoa,
)
from jogo.quests import quests_da_lorena, quests_do_eivor
from jogo.save import carregar_jogo_tela, existe_saves, salvar_jogo, saves
from jogo.tela.imprimir import Imprimir
from jogo.tela.menu import Menu

tela = Imprimir()


class JogoController:
    def __init__(self, nomes: list[str]):
        self.nomes = nomes
        self.personagem = None
        self.npcs = None
        self.nome_do_jogo = ""

    def novo_jogo_saves(self):
        mensagens = {
            str(numero): mensagem
            for numero, mensagem in enumerate(
                ["novo jogo", "carregar jogo", "deletar jogo"], 1
            )
        }
        self.finalizado = False
        resposta = ""
        while not self.finalizado:
            while not resposta in mensagens:
                tela.limpar_tela()
                for numero, mensagem in mensagens.items():
                    tela.imprimir(f"{numero} - {mensagem}\n", "cyan")
                tela.imprimir("Deseja qual opção: ", "cyan")
                resposta = tela.obter_string()
            resposta = mensagens[resposta]
            if resposta == "carregar jogo":
                self.carregar_jogo()
            elif resposta == "novo jogo":
                self.novo_jogo()
            elif resposta == "deletar jogo":
                self.deletar_jogo()

    def carregar_jogo(self):
        if existe_saves():
            personagens = carregar_jogo_tela(self.nomes)
            tela.imprimir("jogo carregado", "cyan")
            personagens_, nome_do_save = personagens
            self.personagem, *self.npcs = personagens_
            self.nome_do_jogo = nome_do_save
            sleep(2)
            self.finalizado = True
        else:
            tela.imprimir("Não há saves para carregar.", "cyan")
            sleep(3)

    def novo_jogo(self):
        azura = Pessoa("Azura")
        quests = [quest(azura.nome) for quest in quests_da_lorena]
        azura.receber_quest(quests)
        eivor = Pessoa("Eivor")
        quests = [quest(eivor.nome) for quest in quests_do_eivor]
        eivor.receber_quest(quests)
        tavon = Banqueiro("Tavon")
        personagem = self.novo_personagem()
        nome_jogo = ""
        arquivos = [arquivo.name for arquivo in Path().glob("*.pkl")]
        arquivos.append(".pkl")
        while not bool(nome_jogo) or nome_jogo + ".pkl" in arquivos:
            tela.limpar_tela()
            tela.imprimir("Qual é o nome do seu save?: ", "cyan")
            nome_jogo = tela.obter_string()
            if nome_jogo + ".pkl" in arquivos:
                tela.imprimir("Erro: nome do arquivo existente", "vermelho")
                sleep(3)
        npcs = [azura, eivor, tavon]
        nome_jogo += ".pkl"
        salvar_jogo(personagem, npcs, nome_jogo)
        self.personagem = personagem
        self.npcs = npcs
        self.nome_do_jogo = nome_jogo
        self.finalizado = True

    def deletar_jogo(self):
        if existe_saves():
            nomes_saves = saves()
            nomes_dict = {str(x): y for x, y in enumerate(nomes_saves, 1)}
            qual_jogo_deletar = ""
            while not qual_jogo_deletar in nomes_dict:
                tela.limpar_tela()
                for numero, arquivo in nomes_dict.items():
                    tela.imprimir(f"{numero} - {arquivo[:-4]}\n", "cyan")
                tela.imprimir(f"Deseja deletar qual jogo?: ", "cyan")
                qual_jogo_deletar = tela.obter_string()
            tela.limpar_tela()
            tela.imprimir(
                "Tem certeza que deseja deletar o save? [s/n/sim/não]: ",
                "cyan",
            )
            tem_certeza = tela.obter_string()
            if tem_certeza in ["s", "sim"]:
                arquivo = Path(nomes_dict[qual_jogo_deletar])
                arquivo.unlink()
                tela.imprimir("Save deletado", "cyan")
                sleep(2)
        else:
            tela.imprimir("Não existe saves.", "cyan")
            sleep(2)

    def novo_personagem(self):
        nome = ""
        while not bool(nome):
            tela.limpar_tela()
            tela.imprimir("qual é o nome do seu personagem?: ", "cyan")
            nome = tela.obter_string()
        classes = [
            Arqueiro,
            Guerreiro,
            Mago,
            Assassino,
            Clerigo,
            Monge,
            Druida,
        ]
        classes_nomes = [
            "Arqueiro",
            "Guerreiro",
            "Mago",
            "Assassino",
            "Clerigo",
            "Monge",
            "Druida",
        ]
        classes_dict = dict(zip(classes_nomes, classes))
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

    def retornar_personagem(self):
        return self.personagem

    def retornar_npcs(self):
        return self.npcs

    def retornar_nome_do_jogo(self):
        return self.nome_do_jogo


def main():
    nome_das_pessoas_que_tem_que_salvar = [
        "Personagem",
        "Azura",
        "Eivor",
        "Tavon",
    ]
    jogo = JogoController(nome_das_pessoas_que_tem_que_salvar)
    jogo.novo_jogo_saves()
    personagem = jogo.retornar_personagem()
    azura, eivor, tavon = jogo.retornar_npcs()
    nome_jogo = jogo.retornar_nome_do_jogo()
    bram = ComercianteItemQuest(
        "Bram", [Draconica], [ItemQuest("Coração de Dragão")]
    )
    hagar = Ferreiro("Hagar")
    itens = curas + roupas_draconicas
    farkas = Comerciante("Farkas", itens)
    menu = Menu(personagem, nome_jogo)
    menu.obter_npcs([azura, farkas, tavon, eivor, bram, hagar])
    menu.ciclo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()
