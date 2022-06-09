from jogo.tela.imprimir import Imprimir

tela = Imprimir()


class Quest:
    def __init__(self, descricao, valor, xp, item):
        self.descricao = descricao
        self.valor = valor
        self.item = item
        self.xp = xp

    def pagar(self, personagem):
        """Método que paga o personagem."""
        personagem.pratas += self.valor

    def depositar_xp(self, personagem):
        """Método que dá o xp para o personagem."""
        personagem.experiencia += self.xp


def quest_gato(nome, personagem, quest):
    """Função que dá a quest para o gato."""
    tela.imprimir(
        f'{nome}: Faz tempo que não vejo meu gatinho, acho que o perdi. '
        'Ele sempre vai brincar na floresta. Traga ele para mim'
        ' que eu te dou dinheiro.\n', 'cyan'
    )
    tela.imprimir('deseja aceitar a quest? s/n: ', 'cyan')
    resposta = tela.obter_string().lower()
    if resposta in ['s', 'sim']:
        personagem.quests.append(quest)
        return True
    return False
