from jogo.tela.imprimir import Imprimir


tela = Imprimir()


class Vilarejo:
    def __init__(self, nome: str, personagem, npcs: list):
        self.nome = nome
        self.npcs = npcs
        self.personagem = personagem

    def explorar(self):
        for npc in self.npcs:
            tela.limpar_tela()
            tela.imprimir(f"deseja interagir com {npc}? [s/n]: ")
            resposta = tela.obter_string().lower()
            if resposta in ['s', 'sim']:
                npc.interagir(self.personagem)
