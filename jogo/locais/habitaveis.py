from jogo.tela.imprimir import Imprimir
from jogo.utils import chunk

tela = Imprimir()


class Vilarejo:
    def __init__(self, nome: str, personagem, npcs: list):
        self.nome = nome
        self.personagem = personagem
        self.npcs_dict = {str(x): y for x, y in enumerate(npcs)}
        tabela = [f"{numero} - {npc}" for numero, npc in self.npcs_dict.items()]
        self.tabela_cortada = chunk(tabela, 18)

    def explorar(self):
        numero = self._obter_numero('Deseja interagir com qual npc?: ')
        while (
            numero.isnumeric() and
            bool(numero) and numero in self.npcs_dict
        ):
            npc = self.npcs_dict[numero]
            npc.interagir(self.personagem)
            numero = self._obter_numero('Deseja interagir com qual npc?: ')

    def _obter_numero(self, mensagem: str):
        """Método que organiza as páginas para o usuário e retorna um numero."""
        numeros_paginas = {
            f":{n}": n for n in range(1, len(self.tabela_cortada) + 1)
        }
        numero = ':1'
        while numero in numeros_paginas:
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(self.tabela_cortada)} "
                "- Para passar de página digite :numero exemplo-> :2\n",
                'cyan'
            )
            n = numeros_paginas.get(numero, 1)
            for texto in self.tabela_cortada[n -1]:
                tela.imprimir(texto + '\n', 'cyan')
            tela.imprimir(mensagem, 'cyan')
            numero = tela.obter_string()
        return numero
