from jogo.tela.imprimir import Imprimir


tela = Imprimir()


def funcao_quest(nome, personagem, quest):
    tela.imprimir(
        f'{nome}: Faz tempo que não vejo meu gatinho, acho que o perdi.'
    )
    tela.imprimir('Ele sempre vai brincar na floresta. Traga ele para mim')
    tela.imprimir(' que eu te dou dinheiro.\n')
    tela.imprimir('deseja aceitar a quest? s/n: ')
    resposta = tela.obter_string().lower()
    if resposta in ['s', 'sim']:
        personagem.quests.append(quest)
        return True
    return False
